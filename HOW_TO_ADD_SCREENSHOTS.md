# How to Add Screenshots to the Report

## Step 1: Create Screenshots Folder

```bash
mkdir outputs/figures/dashboard
```

## Step 2: Run the Dashboard

Make sure both backend and frontend are running:

**Terminal 1 - Backend:**
```bash
cd dashboard/backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd dashboard/frontend
npm start
```

## Step 3: Take Screenshots

Open the dashboard at http://localhost:3000 and take screenshots of:

### Required Screenshots:

1. **dashboard_overview.png** - Full page view showing all components
2. **statistics_cards.png** - Statistics overview section
3. **price_chart.png** - Price history chart with change points
4. **volatility_chart.png** - Volatility analysis chart
5. **event_timeline.png** - Event timeline with filters
6. **date_filter.png** - Date range filter in action
7. **event_correlation.png** - Event correlation view (filter by change point)

### How to Take Screenshots:

**Windows:**
- Press `Windows + Shift + S` to open Snipping Tool
- Select area to capture
- Save to `outputs/figures/dashboard/`

**Mac:**
- Press `Cmd + Shift + 4` to capture area
- Save to `outputs/figures/dashboard/`

**Browser Extension:**
- Use "Full Page Screen Capture" extension for full-page screenshots

## Step 4: Add Screenshots to Report

Open `FINAL_REPORT.html` and find the section:
```html
<h4>Dashboard Screenshots (Add After Running Dashboard)</h4>
```

Add your screenshots using this format:

```html
<p><strong>Figure 7: Dashboard Overview</strong></p>
<img src="outputs/figures/dashboard/dashboard_overview.png" alt="Dashboard Overview" width="800">
<p><em>Complete dashboard showing statistics, price chart, volatility analysis, and event timeline.</em></p>

<p><strong>Figure 8: Price Chart with Change Points</strong></p>
<img src="outputs/figures/dashboard/price_chart.png" alt="Price Chart" width="800">
<p><em>Interactive price chart with detected change points marked as red dashed lines.</em></p>

<p><strong>Figure 9: Volatility Analysis</strong></p>
<img src="outputs/figures/dashboard/volatility_chart.png" alt="Volatility Chart" width="800">
<p><em>Rolling volatility chart with adjustable window size (30-day shown).</em></p>

<p><strong>Figure 10: Event Timeline</strong></p>
<img src="outputs/figures/dashboard/event_timeline.png" alt="Event Timeline" width="800">
<p><em>Filterable event timeline showing geopolitical events with category badges.</em></p>

<p><strong>Figure 11: Event Correlation View</strong></p>
<img src="outputs/figures/dashboard/event_correlation.png" alt="Event Correlation" width="800">
<p><em>Events correlated with a specific change point, showing proximity scores.</em></p>
```

## Step 5: Verify Images Display

1. Save the HTML file
2. Open `FINAL_REPORT.html` in your browser
3. Scroll to the screenshots section
4. Verify all images display correctly

## Tips for Good Screenshots

### Do:
- ✅ Use full browser width for better visibility
- ✅ Capture clear, high-resolution images
- ✅ Show interactive features (hover tooltips, filters)
- ✅ Include different views (filtered, unfiltered)
- ✅ Capture both overview and detail views

### Don't:
- ❌ Include browser UI (address bar, bookmarks)
- ❌ Capture with low resolution
- ❌ Include personal information
- ❌ Use inconsistent image sizes

## Alternative: Use Existing Figures

If the dashboard isn't running yet, you can use the existing analysis figures:

The report already includes:
- ✅ Brent price trend
- ✅ Price with events
- ✅ Volatility plot
- ✅ Returns distribution
- ✅ ACF/PACF plots
- ✅ Rolling statistics

These are automatically included from `outputs/figures/`

## Troubleshooting

**Images don't display:**
- Check file paths are correct (relative to HTML file)
- Verify image files exist in the specified location
- Check file names match exactly (case-sensitive)

**Images too large:**
- Adjust the `width` attribute: `width="600"` or `width="1000"`
- Or use percentage: `width="100%"`

**Want to add more images:**
- Follow the same format
- Increment figure numbers
- Add descriptive captions

## Example: Complete Screenshot Section

```html
<h3>Dashboard Visualizations</h3>

<p><strong>Figure 7: Complete Dashboard Interface</strong></p>
<img src="outputs/figures/dashboard/dashboard_overview.png" alt="Dashboard" width="800">
<p><em>The interactive dashboard provides a comprehensive view of Brent oil price analysis, 
including statistics, price trends, volatility analysis, and event correlations.</em></p>

<p><strong>Figure 8: Interactive Price Chart</strong></p>
<img src="outputs/figures/dashboard/price_chart.png" alt="Price Chart" width="800">
<p><em>Price history from 1987-2022 with three detected change points marked. 
Hover tooltips show exact prices and events on specific dates.</em></p>

<p><strong>Figure 9: Volatility Analysis Tool</strong></p>
<img src="outputs/figures/dashboard/volatility_chart.png" alt="Volatility" width="800">
<p><em>Rolling volatility with adjustable window sizes (7, 30, 90, 180 days). 
Shows periods of high volatility during crises.</em></p>

<p><strong>Figure 10: Event Timeline and Filtering</strong></p>
<img src="outputs/figures/dashboard/event_timeline.png" alt="Events" width="800">
<p><em>Comprehensive event timeline with category-based filtering. 
Events are color-coded by type (War, Policy, Economic, Supply, Demand).</em></p>

<p><strong>Figure 11: Change Point Correlation Analysis</strong></p>
<img src="outputs/figures/dashboard/event_correlation.png" alt="Correlations" width="800">
<p><em>Detailed view of events correlated with Change Point 1 (August 1990), 
showing proximity scores and temporal relationships.</em></p>
```

---

**Once you have the screenshots, just copy-paste the HTML code above into your report!**
