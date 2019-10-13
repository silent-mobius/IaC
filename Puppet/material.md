# Puppet cert preparation material

### Idempotency

Before we start using Puppet, there are a few core concepts we need to cover. One of these concepts is idempotency, which is when an operation will enforce changes the first time it is run but not any subsequent times. Bash scripts, for example, are not idempotent — if we had a script that installed sysstat:

```bash
#!/bin/bash

apt install sysstat -y
```
The apt install sysstat -y line will run every single time we use the script, even if sysstat already exists on the system.

Puppet works differently, however, because Puppet is idempotent. Let's take a look at some Puppet code that installed sysstat — don't worry if it doesn't make sense yet:

```json
class sysstat {
  package { 'sysstat':
    ensure => installed,
  }
}
```

If we were to run this code against a server managed by Puppet initially — or perform a "Puppet run" — it would install the sysstat package:

```bash
# puppet agent -t
Info: Using configured environment 'production'
Info: Retrieving pluginfacts
Info: Retrieving plugin
Info: Retrieving locales
Info: Loading facts
Info: Caching catalog for ellejaclyn2c.mylabserver.com
Info: Applying configuration version '1554750720'
Notice: /Stage[main]/Sysstat/Package[sysstat]/ensure: created
Notice: Applied catalog in 21.95 seconds
```
Pay attention to the line Notice: /Stage[main]/Sysstat/Package[sysstat]/ensure: created, which signals that we performed the task from our Puppet code and installed sysstat.

But what if we were to run this a second time?:

```bash
# sudo puppet agent -t
Info: Using configured environment 'production'
Info: Retrieving pluginfacts
Info: Retrieving plugin
Info: Retrieving locales
Info: Loading facts
Info: Caching catalog for ellejaclyn2c.mylabserver.com
Info: Applying configuration version '1554750791'
Notice: Applied catalog in 15.94 seconds
```

Notice how that line is missing — that's because Puppet understands that sysstat has already been installed, and it doesn't need to try to install it again.

This idempotency is a defining trait of all configuration management systems — of which Puppet is one. A configuration management system creates a layer of abstraction between the servers you need to manage and the commands you need to run to get the end state you desire. Instead, we describe the desired outcome of our system using whatever language the configuration management tool requires; this description is then used against every server that requires that specific setup, regardless of operating system or distribution. So that sysstat Puppet code, above? We can use that on CentOS as well as Ubuntu. In Puppet, this is due to something called the "resource abstraction layer," which we'll cover in our next lesson.

## Wrap Up

We learned some core traits of configuration management systems, including:
* Configuration management systems are idempotent
* An idempotent operation will make changes the first time it is run, but not any repeating times
* In Puppet, our end state descriptions are idempotent
* Ideally, this description can be used to manage servers regardless of OS or distribution

Now that we have an understanding of these concepts, we can build off this to explore how Puppet achieves idempotency, and see what the language we will be using to actually configure our servers looks like.
