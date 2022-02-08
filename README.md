# repo-updater

**Automation for updating Git and Mercurial Repositories.**  
This Script will search the given folder for repositories and automatically update them.  
It can also be used to commit / push or clean the repos.  
  
How to run:
- create a config.py file like config.py.example
- it can be named however you want
  
To use the updater, run this command:  
<code>
python repo-updater.py config 0
</code>  
insert your config-name | 0 means update, 1 means upload  
 
So you can have multiple configs for different updaters with different folder collections.
(For example, you can have one for work, one for blender-addons, and a private one etc.)

On windows you can create .bat files like the bat.example to get a one click solution.
If you create a shortcut to the .bat you can select one of the given icons and add it to your startup programs.
  
*Note that this is not meant for crazy advanced repo stuff like solving merge conflicts. It's meant for simple pull commit and push tasks.*
