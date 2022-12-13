# Snips

A command-line snippet manager, written in Python.

Execute, store, modify or copy to clipboard code snippets without leaving your favourite terminal.


## Usage

Whole interface is terminal based. You don't have to open anything with external programs.

Snips enables you to:
    
    - copying code snippets into clipboard
    - declare variable arguments in your snippet that can be replaced during execution or changed permanently
    - execute snippet in your OS
    - tag snippets for easier categorizing and retrieval
    - manage configuration
    - store and perform CRUD actions on your snippets
        
Snips is invoked by following command:

`snp --help`

```commandline
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────╮ 
│ add                                                   Create new snippet                                       
│ config                                                Manage configuration                                     
│ edit                                                  Update existing snippet                                  
│ get                                                   Copy snippet value into clipboard                        
│ ls                                                    List all available snippets                              
│ rm                                                    Remove snippet                                           
│ run                                                   Execute snippet in your OS                               
│ show                                                  Show snippet data                                        
│ tags                                                  Manage tags                                              
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────

```
You can declare snippet with arguments that will be interpolated from  `defaults` attribute or asked by prompt during execution or copying to clipboard. 
To do this you have to write `snippet` attribute as

`ls <@arg>directory</@arg>`

Then run it with:

`snp run <alias>` 

(prompt will ask for value of  directory argument)

Or providing arguments upfront:

`snp run <alias> --args directory=/home/guest`

# Installation

For now it's only available by building from source.
Clone this repository then install all dependencies.
Deactivate virtual environment and from root project path run:

`pip install .`

This will install snips into your global python interpreter libs.

[//]: # (### Requirements)
[//]: # ()
[//]: # (`Python` >= 3.8)
[//]: # ()
[//]: # (`pip install snips`)

## Configuration

You can customize snips by changing it's configuration. 

To view possible configuration commands:

`snp config --help`

Configuration contains following attributes:

`CONSOLE_OUTPUT`: manages output display

`DB_PROVIDER`: sets your persistence layer provider.
For now, only file-based document oriented database (provided by TinyDB) is supported, which maps to: `json` value.

`DB_URI`: uri for your database. With `DB_PROVIDER=json` this must be path to .json file.


[//]: # (## Usage Details)

[//]: # (### add)

[//]: # ()
[//]: # (To add new snippet simply:)

[//]: # ()
[//]: # (`snp add`)

[//]: # ()
[//]: # (Then prompt will ask you for all required data.)


[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (### run)

[//]: # ()
[//]: # ()
[//]: # (`snp run <alias>`)

[//]: # ()
[//]: # ()
[//]: # (### get)

[//]: # ()
[//]: # (Default behaviour copies snippet command to clipboard)

[//]: # ()
[//]: # (`snp get <alias>`)

[//]: # ()
[//]: # ()
[//]: # (`snp run <alias>`)

[//]: # ()
[//]: # (### show)

[//]: # ()
[//]: # (Shows details about given snippet)

[//]: # ()
[//]: # (`snp show <alias>`)

[//]: # ()
[//]: # (### remove)

[//]: # ()
[//]: # (Deletes snippet from repository)

[//]: # ()
[//]: # (`snp rm `)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # ()
[//]: # ()
