class Reception:
  def __init__(self):
    self._location = ""
    self._qr = ""
    self._gmaps = ""
    
  def __str__(self):
    nl='\n'
    return f"Location: {self._location}{nl} QR: {self.qr}{nl} GMaps:{self._gmaps}{nl}===="
  
  @property
  def location(self):
    return self._location

  @location.setter
  def location(self, loc):
    self._location = loc
  
  @property
  def qr(self):
    return self._qr

  @qr.setter
  def qr(self, qr):
    self._qr = qr
    
  @property
  def gmaps(self):
    return self._gmaps

  @gmaps.setter
  def gmaps(self, gmaps):
    self._gmaps = gmaps
