ifbytes
=======

Measure and graph network interfaces throughput.

Setup sensor
----------

Run on ifbytes-agent.py on hosts you want to measure. 
Put its output to logs/<hostname>.log file, preferably using ifbytesd.py:

    python ifbytesd.py logs/myhost.log ssh myhost ~/ifbytes-agent.py
    
ifbytesd is a simple wrapper that restarts ssh if it hangs.

Access data
----------

Run server:

    python ifbytes-web.py
    
Access data:

    http://localhost:5000/viewer.html#myhost:eth0:rx,myhost:eth0:tx
