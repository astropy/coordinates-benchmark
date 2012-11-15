pro convert
  seed = 42
  ra = double(randomu(seed, 1000) * 360)
  dec = double(randomu(seed, 1000) * 180 - 90)
  ra = [ra, [0, 0, 0, 90, 90, 90, 180, 180, 180, 270, 270, 270]]
  dec = [dec, [-90, 0, 90, -90, 0, 90, -90, 0, 90, -90, 0, 90]]

  euler, ra, dec, glon, glat, 1
  euler, ra, dec, ecx, ecy, 3

  Bprecess, ra, dec, ra1950, dec1950

  openw, lun, 'coords.txt', /get
  fmt = '((5(d, ", ")), d)'
  printf, lun, '# ra, dec, glon, glat, ecliptic_x, ecliptic_y'
  for i = 0, n_elements(ra) - 1, 1 do begin
     printf, lun,  ra[i], dec[i], glon[i], glat[i], ecx[i], ecy[i], $
             format=fmt
  endfor
  free_lun, lun

end
