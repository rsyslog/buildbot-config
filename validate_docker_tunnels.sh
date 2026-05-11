#!/bin/bash

# Docker Tunnel Validation Script
# Validates SSH tunnel ports and checks Docker server connectivity

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ports to check with their corresponding machine names
declare -A PORT_MACHINES=(
    [20300]="xen rhel (2375)"
    [20301]="xen rhel (2376)"
    [20210]="unknown"
    [20211]="unknown"
    [20200]="unknown"
    [20201]="unknown"
    [20100]="docker1.rsyslog.com (2375)"
    [20101]="docker1.rsyslog.com (2376)"
)

# Ports array
PORTS=(20300 20301 20210 20211 20200 20201 20100 20101)

# Store results
declare -A DOCKER_INFO

print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    Docker Tunnel Validation Report                          ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo
}

print_table_header() {
    echo -e "${YELLOW}┌─────────┬──────────────────────────────┬──────────────┬──────────────────────┬─────────────────┐${NC}"
    echo -e "${YELLOW}│ Port    │ Machine                      │ TCP Connect  │ Docker API            │ Status          │${NC}"
    echo -e "${YELLOW}├─────────┼──────────────────────────────┼──────────────┼──────────────────────┼─────────────────┤${NC}"
}

print_table_footer() {
    echo -e "${YELLOW}└─────────┴──────────────────────────────┴──────────────┴──────────────────────┴─────────────────┘${NC}"
}

check_port() {
    local port=$1
    if netstat -tln | grep -q "127.0.0.1:$port"; then
        return 0
    else
        return 1
    fi
}

test_tcp() {
    local port=$1
    local start_time=$(date +%s%N)
    
    if timeout 5 bash -c "</dev/tcp/127.0.0.1/$port" 2>/dev/null; then
        local end_time=$(date +%s%N)
        local duration=$(( (end_time - start_time) / 1000000 ))
        printf "OK (%dms)" "$duration"
        return 0
    else
        printf "FAILED"
        return 1
    fi
}

test_docker() {
    local port=$1
    local start_time=$(date +%s%N)
    
    local response=$(timeout 10 curl -s --connect-timeout 5 "http://127.0.0.1:$port/version" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$response" ]; then
        local end_time=$(date +%s%N)
        local duration=$(( (end_time - start_time) / 1000000 ))
        local version=$(echo "$response" | grep -o '"Version":"[^"]*"' | cut -d'"' -f4 2>/dev/null | head -1 || echo "Unknown")
        
        DOCKER_INFO[$port]="$response"
        printf "OK (%dms) - %s" "$duration" "$version"
        return 0
    else
        printf "FAILED"
        DOCKER_INFO[$port]=""
        return 1
    fi
}

get_status() {
    local tcp_ok=$1
    local docker_ok=$2
    
    if [ $tcp_ok -eq 0 ] && [ $docker_ok -eq 0 ]; then
        echo -e "${GREEN}● HEALTHY${NC}"
    elif [ $tcp_ok -eq 0 ] && [ $docker_ok -eq 1 ]; then
        echo -e "${YELLOW}● PARTIAL${NC}"
    else
        echo -e "${RED}● FAILED${NC}"
    fi
}

print_docker_details() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                        Docker Server Details                                 ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo
    
    local has_data=false
    
    for port in "${PORTS[@]}"; do
        if [ -n "${DOCKER_INFO[$port]}" ]; then
            has_data=true
            local machine="${PORT_MACHINES[$port]}"
            echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────────────────────────────┐${NC}"
            echo -e "${YELLOW}│ Port $port - $machine                                                              │${NC}"
            echo -e "${YELLOW}├─────────────────────────────────────────────────────────────────────────────────────┤${NC}"
            
            local response="${DOCKER_INFO[$port]}"
            local version=$(echo "$response" | grep -o '"Version":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "Unknown")
            local api_version=$(echo "$response" | grep -o '"ApiVersion":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "Unknown")
            local os=$(echo "$response" | grep -o '"Os":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "Unknown")
            local arch=$(echo "$response" | grep -o '"Arch":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "Unknown")
            local kernel=$(echo "$response" | grep -o '"KernelVersion":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "Unknown")
            local build_time=$(echo "$response" | grep -o '"BuildTime":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "Unknown")
            
            printf "${YELLOW}│${NC} %-20s: %s\n" "Version" "$version"
            printf "${YELLOW}│${NC} %-20s: %s\n" "API Version" "$api_version"
            printf "${YELLOW}│${NC} %-20s: %s\n" "Operating System" "$os"
            printf "${YELLOW}│${NC} %-20s: %s\n" "Architecture" "$arch"
            printf "${YELLOW}│${NC} %-20s: %s\n" "Kernel Version" "$kernel"
            printf "${YELLOW}│${NC} %-20s: %s\n" "Build Time" "$build_time"
            
            echo -e "${YELLOW}└─────────────────────────────────────────────────────────────────────────────────────┘${NC}"
            echo
        fi
    done
    
    if [ "$has_data" = false ]; then
        echo -e "${RED}No Docker servers responded successfully.${NC}"
        echo
    fi
}

main() {
    print_header
    
    local total_ports=${#PORTS[@]}
    local healthy=0
    local partial=0
    local failed=0
    
    print_table_header
    
    for port in "${PORTS[@]}"; do
        local machine="${PORT_MACHINES[$port]}"
        
        # Check if port is listening
        if ! check_port $port; then
            printf "│ %-7s │ %-30s │ %-12s │ %-20s │ " "$port" "$machine" "NOT LISTENING" "N/A"
            echo -e "${RED}● FAILED${NC} │"
            ((failed++))
            continue
        fi
        
        # Test TCP connectivity
        tcp_result=$(test_tcp $port)
        tcp_ok=$?
        
        # Test Docker API
        docker_result=$(test_docker $port)
        docker_ok=$?
        
        # Get status
        status=$(get_status $tcp_ok $docker_ok)
        
        # Count results
        if [ $tcp_ok -eq 0 ] && [ $docker_ok -eq 0 ]; then
            ((healthy++))
        elif [ $tcp_ok -eq 0 ] && [ $docker_ok -eq 1 ]; then
            ((partial++))
        else
            ((failed++))
        fi
        
        # Print result
        printf "│ %-7s │ %-30s │ %-12s │ %-20s │ " "$port" "$machine" "$tcp_result" "$docker_result"
        echo "$status │"
    done
    
    print_table_footer
    echo
    
    # Print summary
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                              Summary                                        ║${NC}"
    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════════════════════╣${NC}"
    printf "${BLUE}║${NC} Total Ports: %-3s │ ${GREEN}Healthy: %-3s${NC} │ ${YELLOW}Partial: %-3s${NC} │ ${RED}Failed: %-3s${NC} │ %-15s ${BLUE}║${NC}\n" \
           "$total_ports" "$healthy" "$partial" "$failed" ""
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo
    
    # Print Docker server details
    print_docker_details
    
    # Print timestamp
    echo -e "${YELLOW}Report generated at: $(date)${NC}"
}

# Check dependencies
check_deps() {
    for cmd in netstat curl timeout; do
        if ! command -v $cmd &> /dev/null; then
            echo -e "${RED}Error: Missing required command: $cmd${NC}"
            exit 1
        fi
    done
}

check_deps
main
