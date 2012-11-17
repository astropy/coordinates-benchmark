pro writecol, file, c1, c2
  openw, lun, file, /get
  for i = 0, n_elements(c1) - 1, 1 do begin
     printf, lun, c1[i], c2[i], format='(d, ", ", d)'
  endfor
  free_lun, lun
end

;+
; PURPOSE:
;  Convert J2000 points from coords_j2000.txt into another
;  coordinate system, and write to file
;
; INPUTS:
;  target: The output system. One of 'GALACTIC', 'ECLIPTIC', or
;  'B1950'
;-
pro convert, target
  readcol, '../initial_coords.txt', ra, dec, format='d,d', /silent
  if target eq 'GALACTIC' then begin
     euler, ra, dec, x, y, 1
  endif else if target eq 'ECLIPTIC' then begin
     euler, ra, dec, x, y, 3
  endif else if target eq 'B1950' then begin
     Bprecess, ra, dec, x, y
  endif else $
     message, 'Target must be GALACTIC, ECLIPTIC, or B1950'

  writecol, 'coords_'+strlowcase(target)+'.txt', x, y
end

pro driver
  convert, 'GALACTIC'
  convert, 'B1950'
  convert, 'ECLIPTIC'
end
