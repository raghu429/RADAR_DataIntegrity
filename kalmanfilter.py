import numpy as np

class KalmanFilter:
  """
    A class that predicts the next state of the system given sensor measurements 
    using the Kalman Filter algorithm 

    z measurement
    H measurement function
    P uncertainity covariance
    F state transition matirx
    x estimate
    u motion vector
    
  """

  def __init__(self, n):

    self.n = n
    self.I = np.matrix(np.eye(n))
    self.x = None
    self.P = None
    self.F = None
    self.Q = None
  
  def start(self, x, P, F, Q):
    # print('kalmanfilter: inside start')
    self.x = x
    self.P = P
    self.F = F
    self.Q = Q
        
  def setQ(self, Q):
    self.Q = Q

  def updateF(self, dt):
    self.F[0, 2], self.F[1, 3]  = dt, dt
 
  def getx(self):
    # print('KF getx:', self.x)
    return self.x

  def predict(self):
    # print('**KF:predict', self.x)
    self.x = self.F * self.x
    self.P = self.F * self.P * self.F.T + self.Q
    
  def update(self, z, H, Hx, R):

    y = z - Hx
    PHt = self.P * H.T
    S = H * PHt + R    
    K = PHt * (S.I)
    
    self.x = self.x + K * y
    self.P = (self.I - K * H) * self.P