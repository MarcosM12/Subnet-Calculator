import math

##Error messages
NO_IP_ERR = 'Null IP adrress'
NO_SUBMASK = 'Null subnet mask'
FORMAT_IP_ERR = 'Invalid IP address format (Format: XXX.XXX.XXX.XXX)'
FORMAT_SUBMASK_ERR = 'Invalid Subnet Mask format (Format: XXX.XXX.XXX.XXX)'


# Check if ip address is valid
def check_IP_addr(addr):
    first_oct = True
    if len(addr) == 0:
        return NO_IP_ERR

    else:
        octets = addr.split(".")  # split ip string in four different octets
        if len(octets) != 4:
            return FORMAT_IP_ERR

        for item in octets:
            try:
                if first_oct is True:
                    if not 1 <= int(item) <= 126 \
                            or (128 <= int(item) <= 191 and (int(item) != 169 or int(octets[1]) != 254))\
                            or 192 <= int(item) <= 223:
                        return 'Invalid IP address (must be unicast address)'
                    else:
                        first_oct = False
                else:
                    if not 0 <= int(item) <= 255:
                        return 'Invalid IP address (Octet: ' + str(item) + ' must be between: 0 and 255)'

            except:
                return FORMAT_IP_ERR


# Check if subnet mask is valid
def check_submask(addr):
    if len(addr) == 0:
        return NO_SUBMASK

    else:
        first_oct = True
        valid_masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]
        octets = addr.split(".")  # split ip string in four different octets
        if len(octets) != 4:
            return FORMAT_SUBMASK_ERR

        for item in octets:
            try:
                if first_oct is True:
                    last_item = int(item)
                    if not last_item == 255:
                        return 'Invalid subnet mask (First Octet: ' + str(last_item) + ' must be equal to 255)'
                    first_oct = False
                else:
                    if int(item) in valid_masks and last_item >= int(item):
                        last_item = int(item)
                    else:
                        return 'Invalid subnet mask'
            except:
                return FORMAT_SUBMASK_ERR


# Convert a given address to hexadecimal format
def convert_to_hex(addr):
    addr = addr.split(".")
    converted_ip = ''
    i = 0
    for item in addr:
        converted_ip = converted_ip + ('{:02X}'.format(int(item)))
        if i <= 2:
            converted_ip = converted_ip + "."  # Put dots to maintain IPV4 notation after conversion
        i += 1

    return converted_ip


def calc_wildcard(submask):
    octets = submask.split(".")
    wildcard = ''
    i = 0
    for item in octets:
        wildcard = wildcard + str(255 - int(item))
        if i <= 2:
            wildcard = wildcard + "."  # Put dots to maintain IPV4 notation after conversion
            i += 1

    return wildcard


def convert_to_binary(addr):
    octets = addr.split(".")
    binary_mask = ''
    for item in octets:
        binary_mask += bin(int(item)).lstrip('0b').zfill(8)
    return binary_mask

def convert_to_decimal(bin_addr):
    c = 0
    addr = ''
    for i in range(0, len(bin_addr), 8):
        addr += str(int(bin_addr[i:i + 8], 2))
        if c <= 2:
            addr += '.'
            c += 1
    return addr

def calc_number_hosts(submask):
    submask_bin = convert_to_binary(submask)
    no_of_zeros = submask_bin.count('0')
    return abs(2 ** no_of_zeros - 2)

"""
updates subnet mask based on the number of hosts or 
maximum subnets chose by the user
"""
def update_submask(option, value):
    if option == 'number_hosts': #in this case, value = number of hosts
        no_of_zeros = int(math.log2(value + 2))
        no_of_ones = 32 - no_of_zeros
        bin_submask = '1' * no_of_ones + '0' * no_of_zeros
        return convert_to_decimal(bin_submask)

    elif option == 'maximum_subnets': #in this case, value = maximum subnets
        no_of_ones = int(math.log2(value))
        bin_submask = '1' * (no_of_ones + 8) + '0' * (32-no_of_ones-8)
        return convert_to_decimal(bin_submask)

def calc_network_addr(ip_addr, submask):

    ip_bin = convert_to_binary(ip_addr)
    submask_bin = convert_to_binary(submask)

    n_zeros_submask = submask_bin.count('0')
    n_ones_submask = 32 - submask_bin.count('0') #(total of bits in a ip addr) - number of 0's
    net_addr_bin = "".join(ip_bin[0:n_ones_submask] + '0' * n_zeros_submask)

    return convert_to_decimal(net_addr_bin)


def calc_broadcast_addr(ip_addr, submask):

    ip_bin = convert_to_binary(ip_addr)
    submask_bin = convert_to_binary(submask)

    n_zeros_submask = submask_bin.count('0')
    n_ones_submask = 32 - n_zeros_submask #(total of bits in a ip addr) - number of 0's
    broad_addr_bin = "".join(ip_bin[0:n_ones_submask] + '1' * n_zeros_submask)

    return convert_to_decimal(broad_addr_bin)

def calc_host_range(ip_addr,submask):
    ip_bin = convert_to_binary(ip_addr)
    submask_bin = convert_to_binary(submask)

    n_zeros_submask = submask_bin.count('0')
    n_ones_submask = 32 - n_zeros_submask  # (total of bits in a ip addr) - number of 0's
    last_host = convert_to_decimal("".join(ip_bin[0:n_ones_submask] + '1' * (n_zeros_submask - 1)) + '0')
    first_host = convert_to_decimal("".join(ip_bin[0:n_ones_submask] + '0' * (n_zeros_submask - 1)) + '1')
    return "" + first_host + " - " + last_host

def update_oct_range(net_class):
    if net_class == 'A':
        return '1-126'
    elif net_class == 'B':
        return '128-191'
    elif net_class == 'C':
        return '192-223'

def calc_max_subnets(submask):
    subnet_part = submask[4:len(submask)]
    submask_bin = convert_to_binary(subnet_part)
    n_ones_submask = submask_bin.count('1')
    return 2 ** n_ones_submask
