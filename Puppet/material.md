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

---

# Resource Abstraction

As a configuration management tool, Puppet needs to take our end state descriptions and somehow convert them to work across multiple platforms. To do this, it utilizes something called the resource abstraction layer (RAL), which allows us to write simplified code that Puppet can then take and adapt as needed. After all, think of all the ways our servers can differ: We have different init systems, different package managers, even different commands to add and remove users.

Now let's once more consider the sysstat installation code provided earlier:

```json
class sysstat {
  package { 'sysstat':
    ensure => installed,
  }
}
```

Notice package in the second line: This is our resource type. Part of this resource abstraction layer, a resource type, let's us perform an action regardless of the underlying server. So while this example was written on an Ubuntu 18.04 server, we can just as easily use it on other distributions. In fact, we can get a full list of all the package managers the package resource can use by running the following command:
```bash
# puppet describe package

...

Providers
---------
    aix, appdmg, apple, apt, aptitude, aptrpm, blastwave, dnf, dpkg, fink,
    freebsd, gem, hpux, macports, nim, openbsd, opkg, pacman, pip, pip3,
    pkg, pkgdmg, pkgin, pkgng, pkgutil, portage, ports, portupgrade,
    puppet_gem, rpm, rug, sun, sunfreeware, tdnf, up2date, urpmi, windows,
    yum, zypper
```

Puppet is able to perform this level of abstraction through the use of providers, which are underlying Puppet code created to translate our end states into workable commands for the managed servers. So while we'll never have to manually reference, say, yum, in our descriptions, that's still the manager that installs any packages we need on any servers whose package manager is yum — it's just that Puppet is figuring out the commands and running them for us.

At the time of this writing, Puppet is on version 6.4, and there are 11 core resource types provided with our Puppet master. An additional 13 are added when we install the puppet-agent on our managed servers. In contrast, the oldest version of Puppet that the Puppet Professional tests on is 5.5, which contains 48 modules, the majority of which were Nagios-specific and have since been depreciated. We'll be touching on most of the primary 24 resource types as we go through this course, but don't worry about the details yet — we're still taking a high-level look at Puppet, although we're about to dive deeper.

## Wrap Up

In this lesson, we took a high-level look at how Puppet works in regards to configuration management, learning:

* What the resource abstraction layer is and how it simplifies our work
* How the resource abstraction layer works through the use of resource types
* What a resource type looks like
* How providers exist beneath our resource types to ensure our systems are configured using the correct tools

Now that we know how Puppet works on a basic level, however, we want to take a step deeper to look at how we'll set up our systems to work with Puppet and how Puppet actually goes about taking our end states and making them a reality.
Resources

    [Resource Types List - Puppet 6.4](https://puppet.com/docs/puppet/6.4/type.html)
    [Resource Types List - Puppet 5.5](https://puppet.com/docs/puppet/5.5/type.html)

---

# Puppet Architecture
Puppet uses a "master-agent" setup, where a primary server — known as the Puppet master — stores configuration information that is queried by the agents, which are our managed nodes. This setup is consistent across both versions of Puppet — open source and enterprise — with the caveat that in versions prior to Puppet 6, we had the option of running a standalone Puppet architecture using the Puppet apply application.

To break down everything that Puppet contains, we're going to look at it starting from the components in all Puppet setups, then add on our additional Puppet Enterprise features.

## Master (Open Source and Enterprise)

All Puppet masters are comprised of the Puppet Server and certification authority. The Puppet Server is a Java Virtual Machine and compiles our Puppet code for use on our agents, while the certificate authority lets us manage our master and agent certificates so Puppet is only communicating with hosts we deem safe. We also have the option to add PuppetDB (automatically added in Enterprise), which collects Puppet-generated data and enables some advanced features. PuppetDB can also be accessed by other services that may need Puppet data.

## Agent (Open Source and Enterprise)

The Puppet Agent application needs to be on all nodes we manage with Puppet — including our masters! The Puppet agent runs as a background service and periodically queries for compiled Puppet code from the server to enforce change with. Puppet agents also contain Facter, which records facts about our system that are then passed to the master. We can use these facts in our Puppet code.

## Master of Masters (Puppet Enterprise)

PE adds the concept of a "Master of Masters" — or a Puppet master that contains all the additional features of PE. This includes the Puppet server and certificate authority, as well as role-based access control, orchestration for both multi-tiered applications and on-demand Puppet runs, a node classifier that lets us assign code to managed systems, and a web-based console that lets us manage much of the previously-mentioned tools. The Master of Masters also contains Code Manager and a file sync client, which are used to ensure our Puppet code is consistent across a multi-master setup.

## Compile Masters

Using compile masters is entirely optional — depending on the size of your setup. Using only a Master of Masters, PE supports up to 4,000 nodes, which we can increase by 1,500 to 3,000 per additional master, depending on our PuppetDB limitations. A compile master contains the Puppet Server to compile code and the file sync server to receive and transmit Puppet code to the correct directory.

## Wrap Up

In this lesson, we learned the difference between Puppet Open Source and Puppet Enterprise, and viewed how PE builds off Puppet OS to provide a full-featured platform for managing our nodes. We also learned that:

* A Puppet master coordinates the desired end state of a server with the Puppet agent
* The Puppet Server is the component of the Puppet master that compiles our Puppet code for use
* All nodes managed by Puppet run the Puppet agent application, including the Puppet master itself
* Puppet Enterprise uses a "Master of Masters" which contains additional tools that allow for orchestration, code management, role-based access control, and more
* Puppet Enterprise compile masters run similar to open source Puppet, but also contain a file sync server that receives updated Puppet Code from Code Manager

Now, this might seem like a lot of data at once — because it very much is. However, we'll get more in-depth with each of these tools as we move on through the course, starting in the next lesson by discussing catalog compilation.

---

# The Lifecycle of a Puppet Run

At a high level, we understand that Puppet's resource abstraction layer takes our code and translates it so the agent can configure itself, but how does a Puppet run actually work?

When a Puppet agent queries a master with a puppet agent -t, it begins a catalog compilation process. First, the agent initiates a handshake wherein certification information is shared. Assuming the connection to the master is successful, the master then creates a node object — a combination of information about a node, such as environment, parameters, and classes. Once created, the node object is sent to the agent node.

The agent then makes any changes to the system it needs to enforce this node object, such as switching environments. Oftentimes this object is blank, and the node is configured based on its own parameters.

With the configuration finished, the agent requests a catalog from the master and sends along all facts recorded by **Facter** for the master to use. The master then evaluates the main manifest, which is a mapping of modules — or end-state configurations — to nodes. Once it matches the agent to a set of modules, the master evaluates any variables and data in those modules using facts about the agent and adds them to the catalog. Any modules referenced by other modules but not in the main manifest are also evaluated and added to the catalog.

The catalog is then sent to the agent, which performs any changes described in the modules. If enabled, the agent will send a report to Puppet when finished.

## Wrap Up

We went through all the steps that occur during a Puppet run, including:

* The agent and master complete a handshake and create a connection
* The agent provides the master with facts about its system from Factor
* The master provides the agent with a node object, which it uses to update parameters such as environment, if needed
* The master provides the agent with a compiled catalog
* The agent applies the catalog and returns a report (if reporting is enabled)

And now that we know what Puppet's doing under the hood, we can start to get hands on and set up our environment.

---
