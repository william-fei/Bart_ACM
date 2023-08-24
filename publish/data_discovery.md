# Data Explorations

We'd first visualize the time series of the temperatures of indoor and outdoor at the locations, to understand the distribution, pattern, and trend of the datum.


```python
import pandas as pd
```


```python
outdoor = pd.read_csv('../../data/outdoor-temperature-20220601-0912.csv.zip')
```


```python
outdoor
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_time</th>
      <th>Location</th>
      <th>Temperature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-09-12T23:59:49.000-0700</td>
      <td>S50</td>
      <td>64.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-09-12T23:59:28.000-0700</td>
      <td>S10</td>
      <td>63.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-09-12T23:58:56.000-0700</td>
      <td>W40</td>
      <td>60.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-09-12T23:58:42.000-0700</td>
      <td>A20</td>
      <td>61.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-09-12T23:58:21.000-0700</td>
      <td>C60</td>
      <td>64.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>608553</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>C80</td>
      <td>66.0</td>
    </tr>
    <tr>
      <th>608554</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>C40</td>
      <td>55.9</td>
    </tr>
    <tr>
      <th>608555</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>C30</td>
      <td>55.9</td>
    </tr>
    <tr>
      <th>608556</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>A60</td>
      <td>55.9</td>
    </tr>
    <tr>
      <th>608557</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>A58</td>
      <td>55.9</td>
    </tr>
  </tbody>
</table>
<p>608558 rows × 3 columns</p>
</div>



There might be redundancy. Let's remove the duplicated rows in outdoor.


```python
outdoor = outdoor.drop_duplicates(subset=['_time', 'Location', 'Temperature'], keep='first')
```


```python
outdoor
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_time</th>
      <th>Location</th>
      <th>Temperature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-09-12T23:59:49.000-0700</td>
      <td>S50</td>
      <td>64.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-09-12T23:59:28.000-0700</td>
      <td>S10</td>
      <td>63.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-09-12T23:58:56.000-0700</td>
      <td>W40</td>
      <td>60.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-09-12T23:58:42.000-0700</td>
      <td>A20</td>
      <td>61.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-09-12T23:58:21.000-0700</td>
      <td>C60</td>
      <td>64.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>608553</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>C80</td>
      <td>66.0</td>
    </tr>
    <tr>
      <th>608554</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>C40</td>
      <td>55.9</td>
    </tr>
    <tr>
      <th>608555</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>C30</td>
      <td>55.9</td>
    </tr>
    <tr>
      <th>608556</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>A60</td>
      <td>55.9</td>
    </tr>
    <tr>
      <th>608557</th>
      <td>2022-06-01T00:00:00.000-0700</td>
      <td>A58</td>
      <td>55.9</td>
    </tr>
  </tbody>
</table>
<p>519537 rows × 3 columns</p>
</div>



The number of rows are ruduced from 797422 to 546586


```python
outdoor['Source'] = 'Outdoor'
```

    /tmp/ipykernel_22441/646069649.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      outdoor['Source'] = 'Outdoor'



```python
indoor = pd.read_csv('../../data/indoor-temperature-20220601-0912.csv.zip')
```


```python
indoor
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_time</th>
      <th>Location</th>
      <th>Temperature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>Y10</td>
      <td>76.3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W40</td>
      <td>76.7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W34</td>
      <td>75.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W20</td>
      <td>71.8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W10</td>
      <td>72.9</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>528903</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>A40</td>
      <td>71.4</td>
    </tr>
    <tr>
      <th>528904</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>A20</td>
      <td>70.1</td>
    </tr>
    <tr>
      <th>528905</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>C60</td>
      <td>78.0</td>
    </tr>
    <tr>
      <th>528906</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>C76</td>
      <td>73.5</td>
    </tr>
    <tr>
      <th>528907</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>A30</td>
      <td>69.4</td>
    </tr>
  </tbody>
</table>
<p>528908 rows × 3 columns</p>
</div>




```python
indoor = indoor.drop_duplicates(subset=['_time', 'Location', 'Temperature'], keep='first')
indoor
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_time</th>
      <th>Location</th>
      <th>Temperature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>Y10</td>
      <td>76.3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W40</td>
      <td>76.7</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W34</td>
      <td>75.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W20</td>
      <td>71.8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2022-09-12T23:52:01.000-0700</td>
      <td>W10</td>
      <td>72.9</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>528903</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>A40</td>
      <td>71.4</td>
    </tr>
    <tr>
      <th>528904</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>A20</td>
      <td>70.1</td>
    </tr>
    <tr>
      <th>528905</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>C60</td>
      <td>78.0</td>
    </tr>
    <tr>
      <th>528906</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>C76</td>
      <td>73.5</td>
    </tr>
    <tr>
      <th>528907</th>
      <td>2022-06-01T00:05:01.000-0700</td>
      <td>A30</td>
      <td>69.4</td>
    </tr>
  </tbody>
</table>
<p>528908 rows × 3 columns</p>
</div>



The number of rows in indoor data are reduced from 589056 to 579326


```python
indoor['Source'] = 'Indoor'
indoor['Location'] = indoor['Location'].str[:3]
```


```python
import altair as alt
from altair_data_server import data_server

alt.data_transformers.enable('data_server')
```




    DataTransformerRegistry.enable('data_server')



to enable Altair to plot for more than 5000 rows.

## Plots of Indoor and Outdoor Temperatures at Different Locations


```python
df = pd.concat([outdoor, indoor])
del outdoor, indoor # save unwanted memory
```

Convert the time column to datetime type, and convert the temperature to float type.


```python

df['_time'] = pd.to_datetime(df['_time'])
df['Temperature'] = df['Temperature'].astype(float)
```


```python
alt.Chart(df).mark_line().encode(
    x='_time:T',
    y=alt.Y("Temperature:Q", scale=alt.Scale(domain=[55, 110])),
    color='Source:N',
    tooltip=['Source', 'Temperature']
).facet(
    'Location:N',
    columns = 6
)
```

    /home/yshen/.local/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
      for col_name, dtype in df.dtypes.iteritems():






<div id="altair-viz-3c3b8a9548024074b154e2288928ff07"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-3c3b8a9548024074b154e2288928ff07") {
      outputDiv = document.getElementById("altair-viz-3c3b8a9548024074b154e2288928ff07");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.17.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "4.17.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"url": "http://localhost:49229/77efc608e04424ef43a67deaa624380f.json"}, "facet": {"field": "Location", "type": "nominal"}, "spec": {"mark": "line", "encoding": {"color": {"field": "Source", "type": "nominal"}, "tooltip": [{"field": "Source", "type": "nominal"}, {"field": "Temperature", "type": "quantitative"}], "x": {"field": "_time", "type": "temporal"}, "y": {"field": "Temperature", "scale": {"domain": [55, 110]}, "type": "quantitative"}}}, "columns": 6, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json"}, {"mode": "vega-lite"});
</script>



## Investigate the pattern of the temperature curves

By examming the above line charts visually, we can divide the locations into the following categories:
    
    - outdoor_only :: only with the outdoor data, not of value for the study
    - indoor_only :: only with the indoor data, maybe not of value
    - incomplete :: have significant number of days when there are missing data. These locations might be used for validation, with the portion available. Or, we might extract the portion with both indoor and outdoor temperature available to increase the amount of data for training
    - both_effective_AC :: with temperature both indoor and outdoor available, and showing AC being effective
    - both_ineffective_AC :: with temperature both indoor and outdoor available, and showing AC being ineffective  


```python
# Locations with outdoor temperature only
outdoor_only = ['A10', 'A58', 'C55', 'C70', 'K10', 'K20', 'L10', 'L14', 'M16', 'M60', 'M70', 'R20', 'S10', 'W30', '']

# Locations with indoor temperature only
indoor_only = ['E20', 'L06', 'ODY', 'OHY', 'ORY', 'S06']

incomplete = ['A40', 'C10', 'C76', 'C88', 'E10', 'E39', 'K30', 'L16', 'L18', 'M10', 'M20', 'M30', 'M40', 'M50', 'M80', 'M90', 'M94', 'R10', 'R30,', 'R40', 'R50', 'R60', 'S12', 'S24', 'S26', 'S44', 'W10', 'W20', 'W34', 'W40', 'Y10']
# Locations with both indoor and outdoor temperature
```


```python
both_effective_AC = ['A50', 'A60', 'A70', 'A80', 'A90', 'C30', 'C40', 'C50', 'C54', 'C60', 'C80', 'E30', 'L20', 'L30', 'S20', 'S40', 'S50']

both_ineffective_AC = ['A20', 'A30', 'A70']
```


```python
df_ineffective_AC = df[df['Location'].isin(both_ineffective_AC)]
df_effective_AC = df[df['Location'].isin(both_effective_AC)]
```


```python
df_incomplete = df[df['Location'].isin(incomplete)]

df_indoor_only = df[df['Location'].isin(indoor_only)]
```


```python
del df
```

## Ineffective AC


```python
alt.Chart(df_ineffective_AC).mark_line().encode(
    x='_time:T',
    y=alt.Y("Temperature:Q", scale=alt.Scale(domain=[55, 110])),
    color='Source:N',
    tooltip=['Source', 'Temperature']
).facet(
    'Location:N',
    columns = 6
)
```

    /home/yshen/.local/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
      for col_name, dtype in df.dtypes.iteritems():






<div id="altair-viz-267814f4c853411ca86b9d703e41d408"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-267814f4c853411ca86b9d703e41d408") {
      outputDiv = document.getElementById("altair-viz-267814f4c853411ca86b9d703e41d408");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.17.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "4.17.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"url": "http://localhost:49229/b19a2b13662f0b3fa28ff3a47869d9db.json"}, "facet": {"field": "Location", "type": "nominal"}, "spec": {"mark": "line", "encoding": {"color": {"field": "Source", "type": "nominal"}, "tooltip": [{"field": "Source", "type": "nominal"}, {"field": "Temperature", "type": "quantitative"}], "x": {"field": "_time", "type": "temporal"}, "y": {"field": "Temperature", "scale": {"domain": [55, 110]}, "type": "quantitative"}}}, "columns": 6, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json"}, {"mode": "vega-lite"});
</script>



We might have an issue that the number of locations for ineffective AC as examples for training might be too few.
The solution might be that we need to extract further from the incomplete data set.

## Effective AC


```python
alt.Chart(df_effective_AC).mark_line().encode(
    x='_time:T',
    y=alt.Y("Temperature:Q", scale=alt.Scale(domain=[55, 110])),
    color='Source:N',
    tooltip=['Source', 'Temperature']
).facet(
    'Location:N',
    columns = 6
)
```

    /home/yshen/.local/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
      for col_name, dtype in df.dtypes.iteritems():






<div id="altair-viz-2bc113c636564478a6de81b30d038c34"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-2bc113c636564478a6de81b30d038c34") {
      outputDiv = document.getElementById("altair-viz-2bc113c636564478a6de81b30d038c34");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.17.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "4.17.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"url": "http://localhost:49229/ab5709ce31d4859a05084bc83275f50b.json"}, "facet": {"field": "Location", "type": "nominal"}, "spec": {"mark": "line", "encoding": {"color": {"field": "Source", "type": "nominal"}, "tooltip": [{"field": "Source", "type": "nominal"}, {"field": "Temperature", "type": "quantitative"}], "x": {"field": "_time", "type": "temporal"}, "y": {"field": "Temperature", "scale": {"domain": [55, 110]}, "type": "quantitative"}}}, "columns": 6, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json"}, {"mode": "vega-lite"});
</script>




```python
alt.Chart(df_incomplete).mark_line().encode(
    x='_time:T',
    y=alt.Y("Temperature:Q", scale=alt.Scale(domain=[55, 110])),
    color='Source:N',
    tooltip=['Source', 'Temperature']
).facet(
    'Location:N',
    columns = 6
)
# del df_incomplete
```

    /home/yshen/.local/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
      for col_name, dtype in df.dtypes.iteritems():






<div id="altair-viz-aced34eb67524a2d8835fc4529334505"></div>
<script type="text/javascript">
  var VEGA_DEBUG = (typeof VEGA_DEBUG == "undefined") ? {} : VEGA_DEBUG;
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-aced34eb67524a2d8835fc4529334505") {
      outputDiv = document.getElementById("altair-viz-aced34eb67524a2d8835fc4529334505");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.17.0?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function maybeLoadScript(lib, version) {
      var key = `${lib.replace("-", "")}_version`;
      return (VEGA_DEBUG[key] == version) ?
        Promise.resolve(paths[lib]) :
        new Promise(function(resolve, reject) {
          var s = document.createElement('script');
          document.getElementsByTagName("head")[0].appendChild(s);
          s.async = true;
          s.onload = () => {
            VEGA_DEBUG[key] = version;
            return resolve(paths[lib]);
          };
          s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
          s.src = paths[lib];
        });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else {
      maybeLoadScript("vega", "5")
        .then(() => maybeLoadScript("vega-lite", "4.17.0"))
        .then(() => maybeLoadScript("vega-embed", "6"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"url": "http://localhost:49229/3b170e400c669c72284d18a89a0382b5.json"}, "facet": {"field": "Location", "type": "nominal"}, "spec": {"mark": "line", "encoding": {"color": {"field": "Source", "type": "nominal"}, "tooltip": [{"field": "Source", "type": "nominal"}, {"field": "Temperature", "type": "quantitative"}], "x": {"field": "_time", "type": "temporal"}, "y": {"field": "Temperature", "scale": {"domain": [55, 110]}, "type": "quantitative"}}}, "columns": 6, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json"}, {"mode": "vega-lite"});
</script>



## Consider the difference between indoor and outdoor temperatures

### Case Study: A20

We use location A20 as a case to figure out how to align the indoor and outdoor data by matching roughly their timestamp.


```python
df_A20 = df_ineffective_AC[df_ineffective_AC['Location'] == 'A20']
```


```python
# convert the time stamps to datetime
df_A20['_time'] = pd.to_datetime(df_A20['_time'])
# convert string to float
df_A20['Temperature'] = df_A20['Temperature'].astype(float)
```

    /tmp/ipykernel_22441/3413013261.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df_A20['_time'] = pd.to_datetime(df_A20['_time'])
    /tmp/ipykernel_22441/3413013261.py:4: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      df_A20['Temperature'] = df_A20['Temperature'].astype(float)



```python
df_A20['_time']
```




    3        2022-09-12 23:58:42-07:00
    28       2022-09-12 23:48:33-07:00
    54       2022-09-12 23:38:29-07:00
    81       2022-09-12 23:28:16-07:00
    108      2022-09-12 23:17:43-07:00
                        ...           
    528692   2022-06-01 01:05:01-07:00
    528745   2022-06-01 00:50:01-07:00
    528798   2022-06-01 00:35:01-07:00
    528851   2022-06-01 00:20:01-07:00
    528904   2022-06-01 00:05:01-07:00
    Name: _time, Length: 20221, dtype: datetime64[ns, pytz.FixedOffset(-420)]




```python
# The date of the first data point
# df_A20['_time'].min()
# The date of the last data point
# df_A20['_time'].max()
# The date portion of the first data point
# df_A20['_time'].min().date()
```


```python
#
import datetime
#
df_A20_first_day = df_A20[df_A20['_time'].dt.date == df_A20['_time'].min().date()]
```


```python
df_A20_first_day
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>_time</th>
      <th>Location</th>
      <th>Temperature</th>
      <th>Source</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>602578</th>
      <td>2022-06-01 23:45:00-07:00</td>
      <td>A20</td>
      <td>57.0</td>
      <td>Outdoor</td>
    </tr>
    <tr>
      <th>602611</th>
      <td>2022-06-01 23:30:00-07:00</td>
      <td>A20</td>
      <td>57.0</td>
      <td>Outdoor</td>
    </tr>
    <tr>
      <th>602675</th>
      <td>2022-06-01 23:15:00-07:00</td>
      <td>A20</td>
      <td>57.0</td>
      <td>Outdoor</td>
    </tr>
    <tr>
      <th>602748</th>
      <td>2022-06-01 23:00:00-07:00</td>
      <td>A20</td>
      <td>57.0</td>
      <td>Outdoor</td>
    </tr>
    <tr>
      <th>602801</th>
      <td>2022-06-01 22:45:00-07:00</td>
      <td>A20</td>
      <td>57.0</td>
      <td>Outdoor</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>528692</th>
      <td>2022-06-01 01:05:01-07:00</td>
      <td>A20</td>
      <td>69.3</td>
      <td>Indoor</td>
    </tr>
    <tr>
      <th>528745</th>
      <td>2022-06-01 00:50:01-07:00</td>
      <td>A20</td>
      <td>69.6</td>
      <td>Indoor</td>
    </tr>
    <tr>
      <th>528798</th>
      <td>2022-06-01 00:35:01-07:00</td>
      <td>A20</td>
      <td>69.5</td>
      <td>Indoor</td>
    </tr>
    <tr>
      <th>528851</th>
      <td>2022-06-01 00:20:01-07:00</td>
      <td>A20</td>
      <td>69.6</td>
      <td>Indoor</td>
    </tr>
    <tr>
      <th>528904</th>
      <td>2022-06-01 00:05:01-07:00</td>
      <td>A20</td>
      <td>70.1</td>
      <td>Indoor</td>
    </tr>
  </tbody>
</table>
<p>188 rows × 4 columns</p>
</div>




```python
import pickle

with open('../../data/df_effective_AC.pickle', 'wb') as f:
    pickle.dump(df_effective_AC, f)

with open('../../data/df_ineffective_AC.pickle', 'wb') as f:
    pickle.dump(df_ineffective_AC, f)

with open('../../data/df_A20_first_day.pickle', 'wb') as f:
    pickle.dump(df_A20_first_day, f)

with open('../../data/df_incomplete.pickle', 'wb') as f:
    pickle.dump(df_incomplete, f)

with open('../../data/df_indoor_only.pickle', 'wb') as f:
    pickle.dump(df_indoor_only, f)
```


```python

```
