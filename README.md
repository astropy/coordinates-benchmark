Notes
-----

From David Berry:

> 1) The differences between kapteyn and (idl,pyast,tpm) on the J2000 to
> B1950 tests is reduced seriously if you specify the epoch of
> observation explicitly in kapteyn/convert.py. That is, change
>
> transform_to(skyout='fk4', tag='b1950')
>
> to
>
> transform_to(skyout='fk4,J2000_OBS', tag='b1950')
>
> This reduces the median difference from 0.217 arc-sec, to 0.0044
> arc-sec (this must mean that kapteyn is using a different default
> epoch of observation to the other systems).
>
> 2) Improved agreement in J2000->ecliptic can be achieved by
> specifying the equinox explicitly in kapteyn/convert.py. Change:
>
> transform_to(skyout='ecliptic', tag='ecliptic')
>
> to
>
> transform_to(skyout='ecliptic,J2000', tag='ecliptic')
>
> This causes kapteyn and IDL have zero difference. The kaptyn->pyast
> median difference goes down from 0.04 to 0.036. The remaining
> difference between kapteyn and pyast seems to be down to:
>
> a) DIfferent obliquity models. kaptyn uses the IAU 2000 model, and
> pyast uses the IAU 2006 model.
> b) Different precession models. kaptyn uses IAU 1976 and pyast uses IAU 2006.
>
> Reverting the models used by pyast gives zero difference between
> kapteyn and pyast for the J2000->Ecliptic test

