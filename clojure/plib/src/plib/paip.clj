(ns paip.qinjian.me)

(def append concat)

(defn one-of [coll]
  (list (nth coll (rand (count coll)))))

(defn random-elt [choices]
  (nth choices (rand (count choices))))

(defn Verb [] (one-of '(hit took saw liked)))
(defn Noun [] (one-of '(man ball woman table)))
(defn Article [] (one-of '(the a)))
(defn noun-phrase [] (append (Article) (Noun)))
(defn verb-phrase [] (append (Verb) (noun-phrase)))
(defn sentence [] (append (noun-phrase) (verb-phrase)))

;;;Here are the new functions may shadow the older functions

(defn Adj [] (one-of '(big little blue green adiabatic)))
(defn Adj* []
  (if (= (int (rand 2)) 0)
    nil
    (append (Adj) (Adj*))))

(defn Prep [] (one-of '(to in by with on)))
(defn PP [] (append (Prep) (noun-phrase)))
(defn PP* []
  (if (random-elt '(true nil))
    (append (PP) (PP*))
    nil))

(defn noun-phrase [] (append (Article) (Adj*) (Noun) (PP*)))




;;;
(defstruct name
  :first
  :last)
(struct-map name :first "Jian" :last "Qin")
(deftype Point [x y])
(def p (Point. 10 20))
(println (.y p))

(defrecord Point2 [x y])
(def p (Point2. 11 12))
(def p (fn [a] a))

(defn length [list]
  (let [len (atom 0)]
    (doseq )))

(:x p)
*1
(make-name :first "asdf" :last "gog")
(sentence)







