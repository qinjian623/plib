(ns qinjian.mapbar.com
  (:use 'clojure.java.io))

(def split-re
  #" ")

(defn process-file-by-lines 
  "按行处理文件内容"
  [file-name, func]
  (with-open [rdr (reader file-name)]
    (doseq [line (line-seq rdr)]
      (func line))))

(defn word-count-one-line [token, count-func]
  (let [t token
        f (count-func)]
    (fn ([line] (f (clojure.string/split (clojure.string/trim line) token)))
      ([] (f)))))

(defn word-counter 
  "单词计数, 空参数表返回结果"
  []
  (let [total-count (atom 0)
        words-count (atom {})]
    (fn ([words] (doseq [word words]
                 (do (swap! total-count inc)
                     (if (contains? @words-count word)
                       (swap! words-count assoc word (inc (@words-count word)))
                       (swap! words-count assoc word 1)))))
      ([] (list @total-count @words-count)))))

(defn entropy [count, total]
  "信息熵计算"
  (- 0 (/ (. Math log10 (/ count total)) (. Math log10 2))))

(defn statistics-entropy [file-name]
  "统计单词信息熵"
  (let [f (word-count-one-line split-re word-counter)]
    (process-file-by-lines file-name f)
    (let [total (first (f))]
      (for [[k v] (second (f))]
        (list k (entropy v total))))))


(defn find-new-word [file-name]
  )


(defn extend-list [char-set]
  (map #(take (inc (.indexOf char-set %)) char-set)
       (drop-last char-set)))


(defn sub-index [char-set]
  (if (= () (rest char-set))
    (list char-set)
    (map (fn [new-char-set]
           (map #(concat % (take-last 1 char-set)) 
             (sub-index new-char-set)))
         (extend-list char-set))))
(def sub-index-memo (memoize sub-index))



(defn flatten-sub-index [char-set ]
  (let [flatten-sub-index-memo (memoize flatten-sub-index)]
    (do
      (println "asdf")
      (if (= 1 (count char-set))
        (list char-set) 
        (map #(concat % (list (last char-set)))
             (reduce #(concat %1 %2) []
                     (map flatten-sub-index-memo (extend-list char-set))))))))
(def flatten-sub-index-memo (memoize flatten-sub-index))

(defn flatten-sub-index [ f char-set]
  (do
    (println "asdf")
    (if (= 1 (count char-set))
      (list char-set) 
      (map #(concat % (list (last char-set)))
           (reduce #(concat %1 %2) []
                   (map (f f)  (extend-list char-set)))))))








;;CODE BELOW IS UNIT TEST
(use 'clojure.test)
(deftest 
  (is (= 2 (+ 1 1))))

(sort #(> (last %1) (last %2)) (statistics-entropy "D:/tttsupersmall"))

(run-all-tests)


