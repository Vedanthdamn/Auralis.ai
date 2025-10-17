# How to Clear Browser Cache for Favicon Updates

When updating favicons, browsers often cache the old icon. Here's how to clear the favicon cache across different browsers:

## Google Chrome / Chromium / Edge

### Method 1: Clear All Cache
1. Press `Ctrl+Shift+Delete` (Windows/Linux) or `Cmd+Shift+Delete` (Mac)
2. Select "Cached images and files"
3. Choose time range (select "All time" for complete clearing)
4. Click "Clear data"

### Method 2: Hard Refresh
1. Navigate to the website
2. Press `Ctrl+F5` (Windows/Linux) or `Cmd+Shift+R` (Mac)
3. This forces a reload without cache

### Method 3: Clear Specific Site Data
1. Open Chrome DevTools (`F12` or `Cmd+Option+I`)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

### Method 4: Manual Favicon Cache Clear (Chrome)
1. Navigate to: `chrome://favicon/` or `edge://favicon/`
2. Find your site's favicon URL
3. Clear browsing data for that specific site

## Firefox

### Method 1: Clear Cache
1. Press `Ctrl+Shift+Delete` (Windows/Linux) or `Cmd+Shift+Delete` (Mac)
2. Check "Cache"
3. Click "Clear Now"

### Method 2: Hard Refresh
1. Navigate to the website
2. Press `Ctrl+F5` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Method 3: Clear Specific Site Data
1. Press `Ctrl+I` (Windows/Linux) or `Cmd+I` (Mac) on the page
2. Go to "Security" tab
3. Click "Clear cookies and site data"

## Safari

### Method 1: Clear Cache
1. Go to Safari → Preferences → Privacy
2. Click "Manage Website Data"
3. Search for your website
4. Click "Remove" or "Remove All"

### Method 2: Empty Cache
1. Enable Developer menu: Safari → Preferences → Advanced → Show Develop menu
2. Click Develop → Empty Caches
3. Refresh the page

### Method 3: Hard Refresh
1. Hold `Shift` and click the Reload button
2. Or press `Cmd+Option+R`

## Additional Tips

### Force Favicon Refresh with URL Parameter
If the above methods don't work, you can force the browser to reload the favicon by adding a version parameter:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=2" />
```

Change the version number (`v=2`, `v=3`, etc.) each time you update the favicon.

### Incognito/Private Mode
Open the site in an incognito or private browsing window to see the new favicon without cache interference.

### Delete Favicon Cache Files (Advanced)

**Chrome (Windows):**
```
%LocalAppData%\Google\Chrome\User Data\Default\Favicons
```

**Chrome (Mac):**
```
~/Library/Application Support/Google/Chrome/Default/Favicons
```

**Chrome (Linux):**
```
~/.config/google-chrome/Default/Favicons
```

**Firefox:**
```
# Navigate to about:support
# Click "Open Folder" next to Profile Folder
# Delete the file: favicons.sqlite
```

### Wait for Browser Cache Expiry
Browser favicon caches typically expire after:
- Chrome: 7 days
- Firefox: 7 days
- Safari: Variable

## Testing Your Favicon

After clearing cache, verify your favicon is loading correctly:

1. **In Browser Tab:** Check if the new icon appears in the browser tab
2. **In Bookmarks:** Create a bookmark and verify the icon
3. **Developer Tools:** 
   - Open DevTools (`F12`)
   - Go to Network tab
   - Filter by "favicon"
   - Refresh and verify the new file is being loaded (200 status)
4. **Favicon Checker:** Use online tools like:
   - https://realfavicongenerator.net/favicon_checker
   - https://www.favicon-generator.org/

## Auralis.ai Favicon Configuration

This project uses the following favicon files:

- `/favicon.svg` - Modern SVG favicon (preferred by modern browsers)
- `/favicon-32x32.png` - 32x32 PNG fallback
- `/favicon-16x16.png` - 16x16 PNG fallback
- `/apple-touch-icon.png` - 180x180 for iOS/Safari
- `/android-chrome-192x192.png` - 192x192 for Android
- `/android-chrome-512x512.png` - 512x512 for Android
- `/site.webmanifest` - Web app manifest for PWA support

All files are located in the `/frontend/public/` directory and are properly referenced in `index.html`.

## Browser Cache Prevention During Development

For development, you can disable cache in browser DevTools:
1. Open DevTools (`F12`)
2. Go to Network tab
3. Check "Disable cache"
4. Keep DevTools open while developing

This ensures you always see the latest changes without manual cache clearing.
