(defn min-kv [coll]
  (apply min-key second (map-indexed vector coll)))

(defn exchange-first [x l]
  (exchange x 0 l))

(defn exchange [x y l]
  (let [x-value (nth l x)
        y-value (nth l y)]
    (assoc (assoc l x y-value) y x-value )))

(defn bubble [coll]
  (if (= '() coll)
    nil
    (let [[k v] (min-kv coll)]
      (conj (bubble (pop (exchange-last k coll)))v))))

(time (take 3(bubble [1 2 3 4 2 1 12 1 1239 923493 1029 128 56 97 1 37 96 6 498  23 56 5])))
(time (take 3 (sort [1 2 3 4 2 1 12 1 1239 923493 1029 128 56 97 1 37 96 6 498  23 56 5] )))
(bubble [1 2 3 4 2 1 12 1 1239 923493 1029 128 56 97 1 37 96 6 498  23 56 5])

(assoc [1 2 3 4] 1 10)




(min-kv [4 2 3 4])
(= '() (rest [1]))
(conj nil 1)

(rest (exchange-first 2 [1 3 4 6]))
(exchange-first 2 [1 3 4 6])
(assoc [1 2 3 4] 2 0)
(vector (1 2 3))