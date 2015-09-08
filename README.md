# Sublime Text 3 PHPUnit Skelgen plugin

### Plugin installation (Linux):
```
cd ~/.config/sublime-text-3/Packages/
git clone git@github.com:jamalwsilva/phpunit_skelgen.git
```

### Plugin installation (OSX):
```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
git clone git@github.com:jamalwsilva/phpunit_skelgen.git
```

### Add "phpunit_skelgen" key to your project settings:
```
{
    /* ... */,
    "settings": {
        /* ... */,
        "phpunit_skelgen": {
            "bin": "/usr/local/bin/phpunit-skelgen",
            "bootstrap": "vendor/autoload.php",
            "tests_path": "tests/phpunit/"
        }
    }
}
```

### Register keyboard combination to invoke generate_test command:
- open "Preferences" => "Key bindings - User" and add:
```
[
    /* other bindings */
    { "keys": ["ctrl+k", "ctrl+g"], "command": "generate_test"}
]
```

