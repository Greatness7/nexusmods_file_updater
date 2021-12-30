# Nexus Mods File Updater

This action automates the process of synchronizing files hosted on [Nexus Mods](https://www.nexusmods.com) with your git repository. You really shouldn't use this unless you are exceptionally lazy.

Since the [Nexus Mods API](https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0#/) does not provide such capability, the task is accomplished through browser automation. As such, in order to use the action you will need to pass in your Nexus Mods login credentials via github's [encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) interface (Repository->Settings->Secrets->New Repository Secret). Feel free to audit the action [source code](https://github.com/Greatness7/nexusmods_file_updater/blob/main/action.py) for any security concerns.

This action is deliberately minimal in scope. Editing mod details, adding screenshots, etc, are not supported. Only file updating for pre-existing mod pages is supported.

## Basic Usage

```yaml
on:
  push:
    tags:
      - "[0-9]+.[0-9]+.[0-9]+"
jobs:
  update_nexus_file:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: greatness7/nexusmods_file_updater@v2
        with:
          username: ${{secrets.NEXUS_USERNAME}}
          password: ${{secrets.NEXUS_PASSWORD}}
          game_domain_name: "morrowind"
          mod_id: "49570"
          file_name: "Mod Name"
          file_version: ${{github.ref_name}}
          update_version: true
          file_category: "Main Files"
          new_existing_version: true
          original_file: "Mod Name .*"
          remove_old_version: true
          file_description: "Changelog: https://github.com/username/repository/releases"
          remove_nmm_button: false
          set_as_main_nmm: true
          requirements_pop_up: true
          file_path: "./Mod Name-latest.7z"
```

## Paramaters

All parameters directly correspond to elements of the website's "Manage Files" page.

- **username**

    *The username for your nexus account. Be sure to use github secrets for this!*

- **password**

    *The password for your nexus account. Be sure to use github secrets for this!*

- **game_domain_name** (string)

    *The game domain name for your mod. Must be lower case. Examples: "morrowind", "skyrim", etc.*

- **mod_id** (string)

    *The id of your mod. You can find it in the URL of your mod page. Examples: "19510", "41102", etc.*

- **file_name** (string)

    *The display name for the file.*

- **file_version** (string)

    *The version of the file. You can use `${{github.ref_name}}` to pass the pushed tag name.*

- **update_version** (boolean)

    *Is this the latest version of the mod.*

- **file_category** (string)

    *The file category.*

    *Must be an extact match to one of the following: "Main Files", "Updates", "Optional files", "Old versions", "Miscellaneous" or "Archived"*

- **new_existing_version** (boolean)

    *Is this a new version of an existing file.*

- **original_file** (string)

    *If `new_existing_version` was true, specifies the original file to be replaced.*

    *Must be an exact match of a pre-existing file name and version (joined by a single space).*

    *Example: "My Awesome Mod 1.0.0"*

    *Rather than hard-coding a precise version, you can use a regex pattern.*

    *Example: "My Awesome Mod .\*"*

- **remove_old_version** (boolean)

    *If `new_existing_version` was true, specifies if the original file should be removed.*

    *Note that no files are ever completely removed, they are only set as "Archived".*

- **file_description** (string)

    *The short file description that appears above the download button. 255 character limit.*

- **remove_nmm_button** (boolean)

    *Remove the 'Download with manager' button*

- **set_as_main_nmm** (boolean)

    *Set the file as the main Vortex file*

- **requirements_pop_up** (boolean)

    *Inform downloaders of this mod's requirements before they attempt to download this file*

- **file_path** (string)

    *Path to the file to be uplodated.*

    *Only accepts '.rar', '.zip', '.7z', '.exe', or '.omod' files.*

    *The file size limit is 20GB.*
