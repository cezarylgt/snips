## General info

This is a command line application for managing code snippets written in python and click framework.

## Usage

### add

Adds new snippet. You can provide all needed arguments to create a new snippet with args or create it by stdinput

`snp add <alias>`

### get

Default behaviour copies snippet command to clipboard

`snp get <path>`

### run

Executes code snippet and provides stdout

`snp run <path>`

### show

shows details about given snippet

`snp show <alias>`

### delete

Deletes snippet from repository

`snp delete `

## Namespaces

Namespaces provides functionality of grouping snippets in a nested manner.

### add namespace

`snp ns add powershell`

You can also nest namespaces.

`snp ns add powershell.sql`

To add new snippet inside given namespace

```
snp add powershell.sql.ps-query 

Enter command: invoke-sqlcmd -ServerInstance localhost -IntegratedSecurity
Enter description: query sql-server
Enter modes:
```

### delete namespace






