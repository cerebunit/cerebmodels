| Transcribed but Not-yet Written                                     |                              | File wrtitten in NWB format    |
| --------------------------------------------------------------------| ---------------------------- | ------------------------------ |
| `un_nwbfile.epochs.epochs.data`                                     | **All** epochs               | `w_nwbfile.epochs.epochs.data` |
| `len(un_nwbfile.epochs.epochs.data)`                                | =                            | `len(w_nwbfile.epochs.epochs.data)`|
| `un_nwbfile.epochs.epochs.data[i]`     Note&#11088;i                | Get **i<sup>th</sup>** epoch | `w_nwbfile.epochs.epochs.data[i]`    Note&#11088;i |
| `un_nwbfile.epochs.epochs.data[i][4]`  Note&#11088;4                | its label                    | `w_nwbfile.epochs.epochs.data[i][4]` Note&#11088;4 |
| `un_nwbfile.epochs.epochs.data[i][3]`  Note&#11088;3                | its data                     | `w_nwbfile.epochs.epochs.data[i][3]` Note&#11088;3 |
| returns object, `<ListSlicer>`                                      |                              | returns list with one element which is a tuple whose third element is object `<TimeSeries>` |
| `un_nwbfile.epochs.epochs.data[i][3].data.data`                     | get <TimeSeries> object      | no counterpart |
| Note:<ul> <li>this returns **all** (i.e, for all epochs) `TimeSeries` objects in a list</li> <li>each list element is of the form, a tuple element in the single element list returned by `w_nwbfile.epochs.epochs.data[i][3]`</li> </ul> |
| `un_nwbfile.epochs.epochs.data[i][3].data.data[i]`  Note&#11088;i  | extract tuple | `w_nwbfile.epochs.epochs.data[i][3][0]` Note&#11088;0 |
| Note: since it contains for all the epochs, extraction requires index for desired epoch _i_ | | Note: index 0 for extracting it from the list|
| `un_nwbfile.epochs.epochs.data[i][3].data.data[i][2]` Note&#11088;2 | extract `TimeSeries` object | `w_nwbfile.epochs.epochs.data[i][3][0][2]` Note&#11088;2 |
| `un_nwbfile.epochs.epochs.data[i][3].data.data[i][2].data`          | TimeSeries **data** values | `w_nwbfile.epochs.epochs.data[i][3][0][2].data.value` |
| `un_nwbfile.epochs.epochs.data[i][3].data.data[i][2].timestamps`    | TimeSeries **timstamps** values | `w_nwbfile.epochs.epochs.data[i][3][0][2].timestamps.value` |
| `un_nwbfile.epochs.epochs.data[i][3].data.data[i][2].unit`          | **unit** for data values | `w_nwbfile.epochs.epochs.data[i][3][0][2].unit` |
| `un_nwbfile.epochs.epochs.data[i][3].data.data[i][2].description`   | TimeSeries description | `w_nwbfile.epochs.epochs.data[i][3][0][2].description` |
|<img width=800/>|<img width=200/>|<img width=800/>|

```diff
+ this will be highlighted in green
- this will be highlighted in red
```
