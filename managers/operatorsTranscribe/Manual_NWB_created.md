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

## no title
```
un_nwbfile_<region> = un_nwbfile.get_acquisition(<region_name>)
```
- `un_nwbfile_<region>.data`
- `un_nwbfile_<region>.timestamps`

# Lower-lever use cases
