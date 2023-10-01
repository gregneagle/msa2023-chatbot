With the advent of AutoPkg 2.0, many custom processors that previously relied on `urllib2` in Python 2 will be forced to migrate to Python 3's `urllib`. The transition is not always simple and easy, and writing safe, resilient and well-crafted URL downloading code is still a significant amount of work.

To ease the pain of that process, there's a new base processor class [URLGetter](https://github.com/autopkg/autopkg/wiki/Processor-URLGetter), which can be subclassed by custom processors in order to make use of some simple download functions. **URLGetter is not meant to replace URLDownloader; it is intended to make downloading things as part of a custom processor simpler.** 

If you want to get started, use the next section to get going quickly. If you want a more detailed explanation for what's available, skip to the longer section.

# How to download in a custom processor with URLGetter, the quick way

## Use URLGetter as your Processor's base class
Import URLGetter from autopkglib, and create a processor class that is a subclass of URLGetter:
```
from autopkglib import URLGetter

class MyProcessor(URLGetter):
    input_variables = {
        "url": {
            "required": True,
            "description": "URL to fetch something from.",
        }
    }
```

## Use self.download() function to store the HTTP result in a variable
In your custom processor, you can use URLGetter's convenience functions to get exactly what you need.

[`self.download(url)`](https://github.com/autopkg/autopkg/blob/master/Code/autopkglib/URLGetter.py#L204-L210) provides a simple function that takes a URL and gives you the resulting output.
```
def main(self):
  # Use curl to fetch a URL and store the result in a variable.
  # Ideal for fetching structured data (JSON or XML), not ideal for storing large downloads
  my_url = self.env["url"]
  data = self.download(url)
```

## Use self.download_to_file() to download a file to disk
In some cases, you'll need to download a file directly to disk inside a custom processor. You can use [`self.download_to_file(url, filename)`](https://github.com/autopkg/autopkg/blob/master/Code/autopkglib/URLGetter.py#L212-L221), which downloads a file to the path you provide:
```
def main(self):
  # Use curl to download a file to disk.
  # Ideal for zipped or archived files that contain information you need, 
  # such as versions or URLs of other downloads
  my_url = self.env["url"]
  filename = os.path.join(self.env["RECIPE_CACHE_DIR"], "downloads", "my_downloaded_filename")
  self.download_to_file(url, filename)
  # Now we can do something with the file, such as read it, rename it, store it in an output variable, etc.
```


# Advanced usage and detailed explanation of URLGetter

## Creating a subclass

When you are creating a custom processor, most of the time the class is a subclass of [Processor](https://github.com/autopkg/autopkg/blob/34874d2f1f91dadfdafaaf5aba63f8231936657f/Code/autopkglib/__init__.py#L391), such as in the [MozillaURLProvider](https://github.com/autopkg/recipes/blob/25518b9b761f943d4c567fcb0944561b32ca3b89/Mozilla/MozillaURLProvider.py#L42):
```
from autopkglib import Processor

class MozillaURLProvider(Processor):
```

By using `URLGetter` as the base class, you inherit access to all of URLGetter's class methods - such as those listed above, like `download()` and `download_to_file()`. For example, [BareBonesURLProvider in autopkg-recipes](https://github.com/autopkg/recipes/blob/master/Barebones/BarebonesURLProvider.py#L20-L33) does this:
```
from autopkglib import ProcessorError
from autopkglib.URLGetter import URLGetter

...

class BarebonesURLProvider(URLGetter):
```

## Advanced usage of the convenience functions download() and download_to_file()
### Custom headers
Both functions have an optional argument `headers`, which allows you to pass custom headers to the curl command, such as in [AdobeReaderURLProvider in autopkg-recipes](https://github.com/autopkg/recipes/blob/25518b9b761f943d4c567fcb0944561b32ca3b89/AdobeReader/AdobeReaderURLProvider.py#L72-L74):
```
        request_url = base_url % (os_version, language)
        header = {"x-requested-with": "XMLHttpRequest"}
        json_response = self.download(request_url, headers=header)
```

### Using text mode with download()
If you are reading in simple plain text from a URL, you can use the `text=True` argument to `self.download()` in order to get back a string value of the result, such as in [AdobeReaderURLProvider in autopkg-recipes](https://github.com/autopkg/recipes/blob/25518b9b761f943d4c567fcb0944561b32ca3b89/AdobeReader/AdobeReaderUpdatesURLProvider.py#L98):
```
        url = AR_UPDATER_BASE_URL + AR_URL_TEMPLATE % major_version
        version_string = self.download(url, text=True)
```

The main difference is that the output of the curl command is turned into standard Python string text, as opposed to binary data. In AutoPkg 2 (and thus, Python 3), this means that the data type is a string value as opposed to a byte sequence (if `text=False`).

You can test this directly in the Python 3 interpreter, using a curl command similar to what would happen above:
```
>>> data = subprocess.run(["curl", "--silent", "--compressed", "--location", "https://armmf.adobe.com/arm-manifests/mac/11/current_version_url_template.txt"], capture_output=True, bufsize=1, text=True)
>>> type(data.stdout)
<class 'str'>
>>> data = subprocess.run(["curl", "--silent", "--compressed", "--location", "https://armmf.adobe.com/arm-manifests/mac/11/current_version_url_template.txt"], capture_output=True, bufsize=1)
>>> type(data.stdout)
<class 'bytes'>
```

The string vs. bytes difference may make it easier to handle the resulting output in your processor.

## Bring your own building blocks with self.download_with_curl(curl_cmd)
If the two convenience functions above aren't sufficient, you can construct your own curl command from scratch and execute it directly using [`download_with_curl()`](https://github.com/autopkg/autopkg/blob/master/Code/autopkglib/URLGetter.py#L183-L190). It also takes in the `text` argument for giving you either string or byte results.

Both `download()` and `download_to_file()` call this function under the hood, but if you don't want to use any of the conveniences, you can roll your own, potentially using the other utility functions listed in the next section.

## Some other helpful utilities
In order to make constructing requests easy, URLGetter also provides some nice convenience functions that you can use:

### Figuring out where curl is
`curl_binary()` looks for what copy of curl to actually execute, in the following order:
* defaults to the environment variable for `CURL_PATH`
* a preference for CURL_PATH (either passed in with `--prefs` or from macOS preferences)
* the first `curl` found in the PATH (similar to typing `which curl` in your Terminal)
* `/usr/bin/curl`

### Adding headers and curl options from preferences
Headers that are passed in through the environment variable `request_headers` are processed using `add_curl_headers()`.

If you have custom options for curl in the environment variable `curl_opts` are also added directly to the curl command. This can be used to add proxy support, or any custom settings required for your environment.