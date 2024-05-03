(import decimal [Decimal])
(import itertools [takewhile])

(require hyrule.anaphoric :readers [%])

(defreader D
  (.slurp-space &reader)
  (assert  (.peek-and-getc &reader "\""))
  (let [decimal-chars-list
        (takewhile (fn [c] (!= "\"" c)) (.chars &reader))

        decimal-string
        (.join "" decimal-chars-list)]

    `(Decimal ~decimal-string)))