# transfer_photos
Code for transferring photos automatically from camera sd card to computer
Forked from JohannesNE/importphotos gist

Added the check for image exif date for creating corresponding folder in destination;
Pictures are copied to folders based on the date they were created.

Also added the check for duplicate files in destination, meaning if the file exists, it will
be skipped before copying.
