(import decimal [Decimal])
(import math)

(require ptf.util :reader [D])

(setv
  MINS "\u2032"
  SECS "\u2033")

(defclass Pace []
  "Represents a pace per some unit distance (i.e. typically time per km.)

  Minimum resolution is seconds, and can support arbitrary fractional-second
  resolution.

  Stored internally as a Decimal quantity of seconds.
  "

  (defn __init__ [self seconds]
    (setv (. self seconds) (Decimal seconds)))

  (defn __str__ [self]
    (let [mm (math.floor (/ self.seconds 60))
          ss (- self.seconds (* mm 60))]
      f"{mm}{MINS}{ss :02f}{SECS}")))
