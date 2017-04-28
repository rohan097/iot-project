# iot-project
## An API for controlling your Raspberry Pi remotely

**Language:** Python

**Framework:** Flask

|   Route   |   Type    |   Command   |   Use   |   Return Code  |  Return Format   |
|:---------:|:----------|:-----------:|:-------:|:-------------:|:----------------:|
|/|GET|-|Check if connected|200|{'Result' : 'Connected'}|
|/devices|GET|-|View all Devices|-|{ "devices": [{"ID": \<int\>,"Location": \<string\>,"Pin": \<int\>,"Status": \<bool\>,"Title": \<string\>}]}|
|/devices/<int>|GET| - | View a particular Device|404 - if not found|{"ID":\<int\>,"Location": \<string\>,"Pin": \<int\>,"Status": \<bool\>,"Title": \<string\>}|
|/devices/|POST|{"Title": \<string\>,	"Location": \<string\>,"Pin": \<int\>}|Add a new device|400 - if any one component is missing, 201 - if Successful|{'Result' : 'Successful'}|
|/devices/\<int\>|POST|{"Title": \<string\>, "Pin": \<int\>, "Location": \<string\>}|Modify a device|404 - if device not found|{'Result' : 'Successful'}|
|/devices/\<int\>|DELETE|-|Delete a device|404 - if not found|{'Result' : 'Successful'}|
|/devices/switch/\<int\>|PUT|-|Toggle a particular device|404 - if not found|{'Result' : 'Successful'}|
|/devices/switch/On|POST|-|Switch on all devices|-|{'Result' : 'Successful'}|
|/devices/switch/Off|POST|-|Switch off all devices|-|{'Result' : 'Successful'}|

----

### Errors

|   Return Code   |   Return Format   |
|:---------------:|:-----------------:|
|401|{'Error' : 'Unauthorized Access'}|
|400|{'Error' : 'Incomplete Parameter'}|
|404|{'Error' : 'Not Found'}|
