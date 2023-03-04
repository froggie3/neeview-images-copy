# neeview-images-copy

Copy all the images in the specific NeeView playlist.

This tool is just for my satisfaction, made for preparing my dataset for LoRA.  

## Notes

* intended to be used in a windows environment
* but it should work with other operating systems (not tested btw)

## Usage

List available playlist files in the playlist directory for NeeView,  which is hardcoded in the source code:

You will probably change this line as you need

```python
playlistsDir = r"C:\mnt1\utl\NeeView\Playlists"
```

Example:
```plain
$ python3 image.py ls

Listing C:\path\to\NeeView\Playlists...

  ...
  ... 
```

Copy images listed in the playlist file.

* Images are saved in the current diretory, but you can change with `--parent` option.

Example:
```plain
$ python3 image.py run <specific_tag> 

playlist from: C:/path/to/NeeView/Playlists/specific_tag.nvpls
           to: C:/Users/foo/Desktop/neeview_imagescopy/specific_tag

making a new directory..... (0.8%)
copying yourimage.jpg ... finished (100.0%)

opening the directory with explorer...
Listing C:\path\to\NeeView\Playlists...
```

