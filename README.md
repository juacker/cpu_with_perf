A quick [Komlog](https://www.komlog.io) example for monitoring *Instructions per cycle*
metric, obtained with the *perf stat* command. Create a transfers block in your komlogd
configuration pointing to *perf_stat.py* file and run komlogd.

This example will create two transfer methods, the first one will execute the *perf stat* command periodically
and store the output to uri *tmp.commands.perf*. The second one will calculate *%CPU* from *ipc* variable.

![Screenshot](https://cloud.githubusercontent.com/assets/2930882/26283443/046564be-3e29-11e7-86ca-ea1132932f00.png)

You can read a related blog post (in spanish) [here](https://medium.com/p/ae43241b6e5b)

![Screenshot](https://cloud.githubusercontent.com/assets/2930882/26277717/d32bdafe-3d8d-11e7-9c77-23713c154495.png)
