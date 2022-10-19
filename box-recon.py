import optparse
import os
import libtmux


    #     ▄▄▄▀▄▄▄
    #▄▄▀▀▀       ▀▀▄▄▄
    #█▀▀▄▄         ▄▄▀▀█    █  █         ▐▌     ▄█▄ █          ▄▄▄▄
    #█    ▀▀▀▄▄▄▀▀▀    █    █▄▄█ ▀▀█ █▀▀ ▐▌▄▀    █  █▀█ █▀█    █▌▄█ ▄▀▀▄ ▀▄▀
    #█        █        █    █  █ █▄█ █▄▄ ▐█▀▄    █  █ █ █▄▄    █▌▄█ ▀▄▄▀ █▀█
    #█        █        █
    #█        █        █    P  E  N   -   T  E  S  T  I  N  G     L  A  B  S
    #▀▀▄▄     █     ▄▄▀▀
    #    ▀▀▀▄▄█▄▄▀▀▀



### WRITTEN BY KAEL AND ASGER


def create_session(box, ip):

    parent_dir = "/home/kael/Desktop/HTB/" # Change this to the directory of where your HTB folders are stored in.
    path = os.path.join(parent_dir, box)
    try:
        os.mkdir(path)
        print("[*] Folder '{}' created.".format(path))
    except:
        print("[X] Folder {} already exists.".format(path))
        exit()

    server = libtmux.Server()

    session = server.new_session("MAIN")

    nmap = session.new_window("NMAP")
    ferox = session.new_window("FEROX")
    nikto = session.new_window("NIKTO")

    nmap_pane = nmap.attached_pane
    ferox_pane = ferox.attached_pane
    nikto_pane = nikto.attached_pane

    nmap_pane.send_keys('cd %s' % path, enter=True)
    nmap_pane.send_keys('nmap -sC -sV -T4 -p- %s -oN %s/nmap' % (ip, path), enter=True)
    ferox_pane.send_keys('cd %s' % path, enter=True)
    ferox_pane.send_keys('feroxbuster --url http://%s --wordlist /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --output %s/ferox_main' % (ip, path),  enter=True)
    nikto_pane.send_keys('cd %s' % path, enter=True)
    nikto_pane.send_keys('nikto -host http://%s -output %s/nikto_main.txt' % (ip, path), enter=True)



def main():
    parser = optparse.OptionParser()

    parser.add_option("--box", dest="box", type="string", \
            help="Specify the box name.")

    parser.add_option("--ip", dest="ip", type="string", \
            help="Specify the port of the box.")

    (options, args) = parser.parse_args()

    if (options.box == None) | (options.ip == None):
        print("You haven't specified a box name and an address, try again.")
    else:
        os.system("tmux kill-server")
        tbox = options.box
        taddress = options.ip
        create_session(tbox, taddress)
        os.system("tmux attach")


if __name__ == '__main__':


    main()
