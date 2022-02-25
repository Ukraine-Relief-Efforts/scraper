class Reception:
  def __init__(self):
    self._location = ""
    self._qr_url = ""
    self._gmaps = ""

  def __str__(self):
    nl='\n'
    return f"Location: {self._location}{nl} QR: {self.qr_url}{nl} GMaps:{self._gmaps}{nl}===="
  
  @property
  def location(self):
    return self._location

  @location.setter
  def location(self, loc):
    self._location = loc
  
  @property
  def qr_url(self):
    return self._qr_url

  @qr_url.setter
  def qr_url(self, qr):
    self._qr_url = qr
    
  @property
  def gmaps(self):
    return self._gmaps

  @qr_url.setter
  def gmaps(self, qr):
    self._gmaps = qr
