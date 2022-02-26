class Reception:
  def __init__(self):
    self._name = ""
    self._address = ""
    self._qr = ""
    self._lat = ""
    self._lon = ""
    
  def __str__(self):
    nl='\n'
    return f"Location: {self._address}{nl} QR: {self.qr}{nl} GMaps:{self._gmaps}{nl}===="
  
  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name):
    self._name = name
  
  @property
  def address(self):
    return self._address

  @address.setter
  def address(self, loc):
    self._address = loc
  
  @property
  def qr(self):
    return self._qr

  @qr.setter
  def qr(self, qr):
    self._qr = qr
    
  @property
  def lat(self):
    return self._lat

  @lat.setter
  def lat(self, lat):
    self._lat = lat

  @property
  def lon(self):
    return self._lon

  @lon.setter
  def lon(self, lon):
    self._lon = lon
