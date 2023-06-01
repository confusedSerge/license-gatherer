# License Gatherer

A small Python script to gather all licenses of a node project and put them into a `LICENSESALL.md` file. 
Note that this was quickly hacked together, hence its capabilities are very limited, i.e. it only works if your project has a `package.json` file and a `yarn.lock` file. It will try to include all licenses of all dependencies, but it might fail if the license is not included in the package. Finally, you have to go through and update the `License: <package license>` line.

I might update this in the future, for example to also fetch the license text from repositories, extend it to other package managers, etc. but for now, this is all it does.

## Usage

To use this script, you need to have Python 3 installed. Then, you can run the script with the following command:

```bash
python3 license-gatherer.py <path-to-project>
```

The script will then create a `LICENSESALL.md` file in the current directory, which contains all licenses of the project in the following format:

```
--------------------------------
Package: <package name>
Version: <package version>
License: <package license>
License Text:

<package license text>

--------------------------------
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](/LICENSE.md) file for details. Note that this only extends to my code and other modules, fonts, etc. are licensed under their respective licenses and do not fall under this license. If you find any license violations, please contact me immediately, as this is not intended.