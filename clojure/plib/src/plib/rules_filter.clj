(require '[clojure.data.csv :as csv]
         '[clojure.java.io :as io])
(defn take-csv
  "Takes file name and reads data."
  [fname]
  (with-open [file (io/reader fname)]
    (doall (map (comp first csv/parse-csv) (line-seq file)))))

(defn qinjian-write-csv
  [fname seq header]
  (with-open [file (io/writer fname)]
    (csv/wirte-csv file seq)))


(defn qinjian-read-csv
  [fname]
  (with-open [file (io/reader fname)]
    (do
     (csv/read-csv file))))
;;(first (qinjian-read-csv "F://short_test.csv"))



(def type-map {2 #(Double/parseDouble %) 
               1 #(Integer/parseInt %) 
               3 (fn [x] x)
               4 #(Long/parseLong %)})

(defn read-csv-lazy-seq
  "Read the csv file info into a lazy seq"
  [fname]
  (csv/read-csv (io/reader fname)))
(defn get-csv-header
  "Read the csv header from the lazy seq, then map in into a <fileder, numb> map"
  [seq]
  (let [first-row  (first seq)]
    (zipmap first-row (range (count first-row)))))

(defn get-csv-body
  "Drop the header line of csv seq"
  [seq]
  (drop 1 seq))

(defn guess-the-type
  "FIXME phone number ....."
  [line]
  (map #(let [item (read-string %)]
          (if (number? item)
            (if (float? item)
              2
              1)
            (3)))
       line))

(defn read-the-type
  [line]
  (map #(cond (= % "int") 1
              (= % "float") 2
              (= % "string") 3
              (= % "bigint") 4
              :else 0)
       line))

(defn parse-line
  [line, types]
  (map #((type-map %2) %1) line types))

(defn condition
  [field, value, op-func, header-map]
  (fn [line]
    (op-func (nth line (header-map field)) value)))

(defn action
  [field, value, header-map]
  (fn [line]
    (assoc (vec line) (header-map field) value )))

;;=========================================================================
(def fname "/mapbar/qinj/short_test.csv")
(def fname "/mapbar/qinj/data/QINJIAN_type_c_utf-8-encode.csv")
(def type ["int", "int", "int", "string", "string", "string","int", "int",
           "float", "float", "float", "float", "string", "string",
           "int", "string", "int", "int", "int", "int","string","string","string","int","string","int","string","int", "int"])
(comment
  (def type ["string", "bigint", "string", "bigint", "string", "string","string", "string",
           "string", "string", "string", "string", "string", "string",
           "string", "string", "int", "string", "string", "int","string","string","string","int","string","int","string","int", "int"]))

(count type)

(def csvseq (read-csv-lazy-seq fname))
(force (parse-line (first (get-csv-body csvseq)) (read-the-type type)))
(take 3 (get-csv-body csvseq))
(def kl (get-csv-header csvseq))
(realized? csvseq)

(def k (range 1000))
(realized? k)
(def l (take 1 k)) 
(def m (drop 1 k)) 
(def k
 (map #(parse-line % (read-the-type type))
      (get-csv-body csvseq)))

(realized? (take 3 (get-csv-body csvseq)))
( (filter #(1) (take 3 (map #(parse-line % (read-the-type type)) (get-csv-body csvseq))) ) )
(seq? (parse-line (first (get-csv-body csvseq)) (read-the-type type)))

(assoc (parse-line (first (get-csv-body csvseq)) (read-the-type type)) 0 "123")
(read-the-type type)
(get-csv-header csvseq)

((action "NID" 123 (get-csv-header csvseq))
 (parse-line (first (get-csv-body csvseq)) (read-the-type type)))

((condition "NID" 910002096 > (get-csv-header csvseq))
 (parse-line (first (get-csv-body csvseq)) (read-the-type type)))

((second csvseq) 0) 
;;(count (filter #((condition "NID" 910002096 > (get-csv-header csvseq)) (parse-line % (read-the-type type)) )(get-csv-body csvseq) )) 
(get-csv-body csvseq) (condition "NID" 910002096 > (get-csv-header csvseq))
(count (get-csv-header csvseq))
(guess-the-type (first (get-csv-body csvseq)))


(take 300 (filter #((condition "POI_ID" 1330005280685 > (get-csv-header csvseq)) (parse-line % (read-the-type type)) )(get-csv-body csvseq) ))

(map (action "KIND" "hellow" (get-csv-header csvseq))
 (take 2 (filter #((condition "KIND" "2283" = (get-csv-header csvseq)) (parse-line % (read-the-type type)))
                   (get-csv-body csvseq)))) 


(def j (filter #((condition "NID" 910002096 > (get-csv-header csvseq)) (parse-line % (read-the-type type)) )(get-csv-body csvseq) ))
(realized? j)
(realized? (doall j))





;;; =====================================================================

(zipmap (get-csv-header (read-csv-lazy-seq fname)) (range 29 ))
(count (take 1 ))
(defn f0 [n] (reduce + (range (inc n))))

(defn f1 [n]
  (let [n (int n)]
    (loop [i (int 1) s (int 0)]
      (if (<= i n) (recur (inc i) (+ i s)) s))))
(time (dotimes [_ 5] (f0 1000000)))
(time (dotimes [_ 5] (f1 100000000)))
(set! *warn-on-reflection* true)
(def a (int-array 10000 (int 5)))
(use '[clojure.java.shell :only [sh]])


(time (amap a idx ret (+ (int 1) (aget a idx))))
;; 795.653779 msecs
(time (amap ^ints a idx ret (+ (int 1) (aget ^ints a idx))))
;; 3.49667 msecs

(defn take-csv
  "Takes file name and reads data."
  [fname]
  (with-open [file (io/reader fname)]
    (csv/parse-csv (slurp file))))


