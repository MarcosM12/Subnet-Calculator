import sys
import random
import PySimpleGUI as sg
import IP_Func

MAX_ERROR_COUNT = 3

def create_gui():
    sg.theme('Dark Tan Blue')
    sg.theme_input_text_color('black')
    sg.theme_input_background_color('white')

    column1 = [[sg.Text("Network Class")],
               [sg.Radio('A', default=True, group_id=1, enable_events=True, key='class_A'),
                sg.Radio('B', group_id=1, enable_events=True, key='class_B'),
                sg.Radio('C', group_id=1, enable_events=True, key='class_C')],
               [sg.Text("IP Address")],
               [sg.Input("1.0.0.0", key='IP', size=(20, 22), justification='center'), sg.Text(' ' * 12)],
               [sg.Text("Subnet Mask")],
               [sg.Input("255.0.0.0", key='sub_mask', size=(20, 22), justification='center')],
               [sg.Text("Maximum Subnets")],
               [sg.Combo(values=[(2 ** i) for i in range(0, 23)], default_value=1, size=(19, 10),
                         key='max_subnets', readonly=True, enable_events=True)],
               [sg.Text("Network Address")],
               [sg.Input("1.0.0.0", key='net_addr', readonly=True, disabled_readonly_background_color='#272727',
                         disabled_readonly_text_color='white', size=(20, 22), justification='center')]
               ]

    column2 = [[sg.Text("First Octet Range")],
               [sg.InputText("1-126", key='First_Oct_Range', readonly=True,
                             disabled_readonly_background_color='#272727',
                             disabled_readonly_text_color='white', size=(20, 22), justification='center')],
               [sg.Text("Hex IP Address")],
               [sg.InputText("01.00.00.00", key='HexIP', readonly=True, disabled_readonly_background_color='#272727',
                             disabled_readonly_text_color='white', size=(20, 22), justification='center')],
               [sg.Text('Wildcard Mask')],
               [sg.Input("0.255.255.255", key='w_mask', readonly=True, disabled_readonly_background_color='#272727',
                         disabled_readonly_text_color='white', size=(20, 22), justification='center')],
               [sg.Text("Hosts per Subnet")],
               [sg.Combo(values=[(2 ** i) - 2 for i in range(2, 25)], default_value=16777214,
                         size=(19, 10), key='n_hosts', enable_events=True, readonly=True)],
               [sg.Text("Broadcast Address")],
               [sg.Input("1.255.255.255", key='broad_addr', readonly=True, disabled_readonly_background_color='#272727',
                         disabled_readonly_text_color='white', size=(20, 22), justification='center')]

               ]

    layout = [[sg.Text(" " * 20),
               sg.Text("Subnet Calculator", text_color='white', font=('Verdana', 20, 'italic'), size=(20, 2))],
              [sg.Column(column1, element_justification='left'),
               sg.Column(column2)],
              [sg.Text("Host Address Range", pad=(178, 5))],
              [sg.Input("1.0.0.1 - 1.255.255.254", key='host_range', readonly=True,
                        disabled_readonly_background_color='#272727',
                        disabled_readonly_text_color='white', size=(52, 22), justification='center')],
              [sg.Button("Calculate", size=(8, 1), pad=(8, 8))],
              [sg.Text(" " * 35), sg.Text("Debug", pad=(0, 0))],
              [sg.Output(size=(50, 10), key='output', pad=(10, 10))]

              ]

    # Create the window
    window = sg.Window(title="Subnet Calculator", layout=layout, margins=(100, 20), font=('Verdana', 12), finalize=True)
    window['IP'].Widget.configure(highlightcolor='red', highlightthickness=1)
    window['sub_mask'].Widget.configure(highlightcolor='red', highlightthickness=1)
    return window


def subnet_calc():
    window = create_gui()
    err_count = 0
    while True:
        event, values = window.read()

        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

        if event == "Calculate" or 'n_hosts' or 'class_A':
            # Update first octet range based on the network class
            if event == 'class_A':
                window.Element('output').Update('')
                window.Element('First_Oct_Range').Update(IP_Func.update_oct_range('A'))
                values['IP'] = "1.0.0.1"
                window.Element('IP').Update(values['IP'])
            elif event == 'class_B':
                window.Element('output').Update('')
                window.Element('First_Oct_Range').Update(IP_Func.update_oct_range('B'))
                values['IP'] = "172.0.0.1"
                window.Element('IP').Update(values['IP'])
            elif event == 'class_C':
                window.Element('output').Update('')
                window.Element('First_Oct_Range').Update(IP_Func.update_oct_range('C'))
                values['IP'] = "192.168.0.1"
                window.Element('IP').Update(values['IP'])

            if IP_Func.check_IP_addr(values['IP']) is not None:
                if err_count < MAX_ERROR_COUNT:
                    print(IP_Func.check_IP_addr(values['IP']))
                    err_count += 1
                else:
                    window.Element('output').Update('')
                    print(IP_Func.check_IP_addr(values['IP']))
                    err_count = 1
                continue
            else:
                window.Element('output').Update('')
                # Convert ip address to hexadecimal notation
                window.Element('HexIP').Update(IP_Func.convert_to_hex(values['IP']))

            if event == 'n_hosts':
                window.Element('output').Update('')
                # Update subnet_mask for this number of hosts
                values['sub_mask'] = IP_Func.update_submask('number_hosts', values['n_hosts'])
                window.Element('sub_mask').Update(values['sub_mask'])

            if event == 'max_subnets':
                window.Element('output').Update('')
                # Update subnet_mask for a given maximum_subnets value
                values['sub_mask'] = IP_Func.update_submask('maximum_subnets', values['max_subnets'])
                window.Element('sub_mask').Update(values['sub_mask'])

            if IP_Func.check_submask(values['sub_mask']) is not None:
                # Output error message
                if err_count < MAX_ERROR_COUNT:
                    print(IP_Func.check_submask(values['sub_mask']))
                    err_count += 1
                else:
                    # Clear Debug window
                    window.Element('output').Update('')
                    print(IP_Func.check_submask(values['sub_mask']))
                    err_count = 1
                continue
            else:
                # Clear Debug window
                window.Element('output').Update('')
                # Calculate wildcard mask using valid subnet mask
                window.Element('w_mask').Update(IP_Func.calc_wildcard(values['sub_mask']))
                # Calculate number of hosts using valid subnet mask
                window.Element('n_hosts').Update(IP_Func.calc_number_hosts(values['sub_mask']))
                window.Element('broad_addr').Update(IP_Func.calc_broadcast_addr(values['IP'], values['sub_mask']))
                window.Element('net_addr').Update(IP_Func.calc_network_addr(values['IP'], values['sub_mask']))
                window.Element('host_range').Update(IP_Func.calc_host_range(values['IP'], values['sub_mask']))
                window.Element('max_subnets').Update(IP_Func.calc_max_subnets(values['sub_mask']))

    window.close()


subnet_calc()
