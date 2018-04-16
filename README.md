# raspberry_pi


    SSHing into pi

    ssh pi@ip_address
    
    get pi's IP address w/ monitor: 
        1. connect pi to monitor
        2. open terminal
        3. hostname -I
    
    get pi's IP address (headless):
        find ip addresses of devices in local network
            arp -a
        try to ssh in until one works; this is your pi

    configuring pi to run scripts automatically at startup

    install requirements in root of pi
        sudo su
        pip3 install -r <absolute_path>/requirements.text
    
    configure startup scripts:
        sudo nano /etc/rc.local
        enter these lines:
        nohup /usr/bin/python3 <absolute_path/my_path.py> > /var/tmp/rclog 2>&1 &
        
        notes:  
            > /var/tmp/rclog 2>&1 sends both stdout and errors to /var/tmp/rclog
            nohup ensures process stays running
            absolute paths are needed because /etc/rc.local runs from root ('/')
            
    error log for /etc/rc.local:
        cat /var/tmp/rclog
        
    check if startup scripts are running:
        ps -ef | grep python
    
    reboot pi:
        sudo reboot