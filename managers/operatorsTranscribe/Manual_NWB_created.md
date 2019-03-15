# High-level use cases
```
un_nwbfile = fab.build_nwdfile(<file_metadata>)
```
## What does this _nwbfile_ have?
- `un_nwbfile.source`
- `un_nwbfile.session_description`
- `un_nwbfile.identifier`
- `un_nwbfile.session_start_time`
- `un_nwbfile.experimenter`
- `un_nwbfile.experiment_description`
- `un_nwbfile.session_id`
- `un_nwbfile.lab`
- `un_nwbfile.institution`

## Get `TimeSeries` objects
### Data & Timestamps
```
un_nwbfile_<region> = un_nwbfile.get_acquisition(<region_name>)
```
- `un_nwbfile_<region>.data`
- `un_nwbfile_<region>.timestamps`
### Stimulus
```
un_nwbfile_stimulus = un_nwbfile.get_stimulus("stimulus")
```
- `un_nwbfile_stimulus.data`
- `un_nwbfile_stimulus.timestamps`


# Low-lever use cases-1
```
nwbts = fab.build_nwbseries(chosenmodel=<model_instance>, tsmd=<ts_metadata>)
```
## What does this have?
- `nwbts[<region_name>].name`
- `nwbts[<region_name>].source`
- `nwbts[<region_name>].data` &#11088;
- `nwbts[<region_name>].unit`
- `nwbts[<region_name>].resolution`
- `nwbts[<region_name>].conversion`
- `nwbts[<region_name>].timestamps` &#11088;
- `nwbts[<region_name>].starting_time`
- `nwbts[<region_name>].rate`
- `nwbts[<region_name>].comments`
- `nwbts[<region_name>].description`
- `nwbts[<region_name>].control`
- `nwbts[<region_name>].control_description`
- `nwbts[<region_name>].parent`

## To add _nwbts_ to _nwbfile_
```
fab.link_nwbseriesresponses_to_nwbfile(nwbts, un_nwbfile)
```

# Low-lever use cases-2
```
un_nwbfile = fab.build_nwbepochs(nwbfile=un_nwbfile, epochmd=<epoch_metadata>, tsmd=<ts_metadata>)
```
## What does this have?
- `un_nwbfile.epochs.epochs.data` all the epochs
- `un_nwbfile.epochs.epochs.data[0][3]` first epoch
- `un_nwbfile.epochs.epochs.data[i][3]` i<sup>th</sup> epoch
- `un_nwbfile.epochs.epochs.data[i][3].data.data[0][2].data`
- `un_nwbfile.epochs.epochs.data[i][3].data.data[0][2].timestamps`
- `un_nwbfile.epochs.epochs.data[i][3].data.data[0][2].unit`
- `un_nwbfile.epochs.epochs.data[i][3].data.data[0][2].description`


# Lower-lever use cases
```
nwbts = fab.generic_timeseries(<ts_metadata>)
```
## What does this have?
- `nwbts.name`
- `nwbts.source`
- `nwbts.data` &#11088;
- `nwbts.unit`
- `nwbts.resolution`
- `nwbts.conversion`
- `nwbts.timestamps` &#11088;
- `nwbts.starting_time`
- `nwbts.rate`
- `nwbts.comments`
- `nwbts.description`
- `nwbts.control`
- `nwbts.control_description`
- `nwbts.parent`

## To add _nwbts_ to _nwbfile_
```
fab.add_acquisition(nwbts)
```
