import socket

from common_ports import ports_and_services


def is_ip(address):
    return not address.split('.')[-1].isalpha()


def to_verbose_results(ip, domain, open_ports):
    verbose_results = []

    verbose_results_header = 'Open ports for '

    # If target is IP address, try to get domain name from IP
    if not domain:
        try:
            domain = socket.gethostbyaddr(ip)[0]
        except socket.error:
            domain = None

    if domain:
        verbose_results_header += '%s (%s)' % (domain, ip)
    else:
        verbose_results_header += ip

    verbose_results_header += '\nPORT     SERVICE'
    verbose_results.append(verbose_results_header)

    # Use the dictionary 'ports_and_services' to get service name
    # for each port
    for port in open_ports:
        if port in ports_and_services:
            service = ports_and_services[port]
        else:
            service = ''

        # Convert port from integer to string and
        # right pad the string with spaces to make its length 4
        port_str = str(port).ljust(4, ' ')
        verbose_results.append('%s     %s' % (port_str, service))

    return verbose_results


def get_open_ports(target, port_range, verbose=False):
    ip = None
    domain = None

    # Ensure IP address is valid
    if is_ip(target):
        try:
            socket.inet_aton(target)
            ip = target
        except:
            return 'Error: Invalid IP address'
    # Ensure domain name is valid
    else:
        try:
            ip = socket.gethostbyname(target)
            domain = target
        except socket.error:
            return 'Error: Invalid hostname'

    first_port = port_range[0]
    last_port = port_range[1]
    open_ports = []

    # Get all open ports in the given range.
    for port in range(first_port, last_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        if not s.connect_ex((ip, port)):
            open_ports.append(port)
        s.close()

    if not verbose:
        return open_ports

    verbose_results = to_verbose_results(ip, domain, open_ports)

    return '\n'.join(verbose_results)