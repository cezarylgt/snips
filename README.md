# Snips

A command-line snippet manager, written in Python.

Execute, store, modify or copy to clipboard code snippets without leaving your favourite terminal.

# Install
## Requirements

`Python` >= 3.8

`pip install snips`

## Usage

Whole interface is terminal based. You don't have to open anything with external programs.

Snips enables you to:
    
    - copying code snippets into clipboard
    - declare variable arguments in your snippet that can be replaced during execution or changed permanently
    - execute snippet in your OS
    - tag snippets for easier categorizing and retrieval
    - manage configuration
    - store and perform CRUD actions on your snippets
        
To call snips:

`snp --help`



### Add

To add new snippet simply:

`snp add`

Then prompt will ask you for all required data.

You can declare snippet with arguments that will be interpolated from  `snippet.defaults` attribute or asked by prompt during execution or copying to clipboard. 

To do this you have to write `snippet.snippet` attribute as

`ls {directory}`

Then run it with:
`snp run :snippet.alias` (prompt will ask for directory argument)

Or providing arguments upfront:

`snp run :snippet.alias --args directory=/home/guest`





### Execute


`snp run :snippet-alias:`


### get

Default behaviour copies snippet command to clipboard

`snp get <path>`


`snp run <path>`

### show

shows details about given snippet

`snp show <alias>`

### delete

Deletes snippet from repository

`snp delete `






