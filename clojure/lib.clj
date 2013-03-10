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

(defn dictionary-counter
  "利用字典计数, 空参数表返回结果，闭包内有副作用"
  []
  (let [total-count (atom 0)
        words-count (atom {})]
    (fn ([words] (doseq [word words]
                 (do (swap! total-count inc)
                     (if (contains? @words-count word)
                       (swap! words-count assoc word (inc (@words-count word)))
                       (swap! words-count assoc word 1)))))
      ([] (list @total-count @words-count)))))

(defn 2-gram-counter
  ""
  ;;TODO 这里2-gram怎么处理？
  []
  (let [2-gram-table (atom {})]))

;;重命名函数，方便别处使用
(def word-counter dictionary-counter)

(defn list-counter
  "利用列表计数，空参数表返回计数结果，闭包内有副作用"
  []
  (let [total-count (atom 0)
        coll (atom ())]
    (fn ([items]
          (doseq [item items]
            ;;TODO 注意，这里是否需要判断list有无重复项目？
            (do (swap! total-count inc)
                (swap! coll concat item))))
      ([] (list @total-count @coll)))))

;;目前有问题
(comment (defn simple-count
           "简单计数，空参数返回计数结果，闭包内有副作用"
           []
           (let [total (atom 0)]
             (fn (swap! total inc)))))


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
  ""
  (let [count-one-line (closure-count-by-line dictionary-counter list-counter)]
    (do (process-file-by-lines file-name count-one-line)
        (let [[[words-count words-count-table]
               [suffix-count suffix-list]
               [reverse-suffix-count reverse-suffix-list]]
              (probability-f)
              ]
          ;;TODO here we go!
          ))))

(defn closure-count-candidate-word [])

(defn closure-count-by-line [word-counter suffix-counter]
  (let [count-words (word-counter)
        count-suffix (suffix-counter)
        count-reverse-suffix (suffix-counter)]
    (fn count-by-line
      ([line]
         (let [words (conj (clojure.string/split (clojure.string/trim line) #" ") "\n")
               words-suffix (suffix-of-list words)
               reverse-words-suffix
               (suffix-of-list
                (conj (clojure.string/split
                       (-> line clojure.string/reverse clojure.string/trim)
                       #" " )
                      "\n"))]
           ;;TODO 这里随后要改写成使用word-counter
           (do
             ;;统计单词数目
             (count-words words)
             ;;统计各后缀数目
             (count-suffix words-suffix)
             (count-reverse-suffix reverse-words-suffix))))
      ([] (list (count-words) (count-suffix) (count-reverse-suffix))))))





(defn statistic-word [all-the-sorted-suffix]
  ;; TODO
  )
(defn suffix-of-list [l]
  ;;TODO 注意与Python版本的不同，还包括列表中最后一个元素单独出现的情况
  (map reverse (extend-list (concat (reverse l) [true]))))



<<<<<<< HEAD
;;小陶的算法验证，程序结果可知，组合的增长率为2^n，未验证程序是否正确
(defn extend-list [char-set]
  "扩展列表方法，可将(1 2 3)，扩展为((1) (1 2))"
  (map #(take (inc (.indexOf char-set %)) char-set) (drop-last char-set)))

(defn flatten-sub-index
  "原始无优化版本"
  [char-set]
  (if (= 1 (count char-set))
    (list char-set) 
    (map #(concat % (list (last char-set)))
         (reduce #(concat %1 %2) []
                 (map flatten-sub-index (extend-list char-set))))))

(defn flatten-sub-index
  "带存储重复结果的算法"
  [f char-set]
  (if (= 1 (count char-set))
      (list char-set) 
      (map #(concat % (list (last char-set)))
           (reduce #(concat %1 %2) []
                   (map (partial f f) (extend-list char-set))))))


;;;这里是Google Group上Yanyi Wan给的
(declare fm)
(defn flatten-sub-index-two
  [char-set]
  (if (= 1 (count char-set))
    (list char-set) 
    (map #(concat % (list (last char-set)))
         (reduce #(concat %1 %2) []
                 (map fm (extend-list char-set))))))
(def fm (memoize flatten-sub-index-two))

(time (count (flatten-sub-index-two (range 1 19))))
(time (count (flatten-sub-index (memoize flatten-sub-index) (range 1 19))))

;;;这里根据上面，包装为一个函数
(defn closure-flatten-sub-index-two [char-set]
  (let [k (declare fm)
        f (fn [char-set]
            (if (= 1 (count char-set))
              (list char-set) 
              (map #(concat % (list (last char-set)))
                   (reduce #(concat %1 %2) []
                           (map fm (extend-list char-set))))))
        j (def fm (memoize f))]
    (f char-set)))
(defn closure-flatten-sub-index-two [char-set]
  (do
    (declare fm)
    (def f (fn [char-set]
             (if (= 1 (count char-set))
               (list char-set) 
               (map #(concat % (list (last char-set)))
                    (reduce #(concat %1 %2) []
                            (map fm (extend-list char-set)))))))
    (def fm (memoize f))
    (f char-set)))

(dotimes [n 5]
  (time (count (closure-flatten-sub-index-two (range 1 19))))) 
(dotimes [n 5]
  (time (count (flatten-sub-index (memoize flatten-sub-index) (range 1 19)))))
;;;TODO 测试可知，下面的实现在性能上快很多，第一次运算会较慢，为什么？
(dotimes [n 5]
  (time (count (flatten-sub-index-two (range 1 19)))))
=======
(defn flatten-sub-index [char-set ]
  (do
    (if (= 1 (count char-set))
      (list char-set) 
      (map #(concat % (list (last char-set)))
           (reduce #(concat %1 %2) []
                   (map flatten-sub-index (extend-list char-set)))))))
(def flatten-sub-index-memo (memoize flatten-sub-index))

(defn flatten-sub-index [f char-set]
  (do
    ;;(println "asdf")
    (if (= 1 (count char-set))
      (list char-set) 
      (map #(concat % (list (last char-set)))
           (reduce #(concat %1 %2) []
                   (map (partial f f)  (extend-list char-set)))))))

(defn a [x y]
  (list x y))
(partial a 1 )







>>>>>>> memoize test sucessed
;;CODE BELOW IS UNIT TEST
(use 'clojure.test)
(deftest 
  (is (= 2 (+ 1 1))))

(sort #(> (last %1) (last %2)) (statistics-entropy "D:/tttsupersmall"))

(run-all-tests)


