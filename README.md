# What is this?
Magerestore is a tool to automate fetching backups from a remote server and unpacking them on a magento installation.

Database import and media folder unzipping is the ony currently supported operations.

Magerestore uses [n98-magerun](https://github.com/netz98/n98-magerun) to handle some tasks, but are not required for all operations.

# How to get started
* Setup non-interactive access to the backups magerestore will interact with. SSH keys are recommended.
* Copy the [magerestore.json](magerestore.json) file to your magento root directory and edit the paths to suit your needs.
* Install the following
   * [n98-magerun](https://github.com/netz98/n98-magerun)
   * `python3-dev` and `build-essentials` (check your package manager)

# Usage
```
cd /your/magento/directory
magerestore restore mysql
magerestore restore media
```
