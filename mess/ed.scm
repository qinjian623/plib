
(define insert-cost
  (lambda (target-i)
    1))
(define delete-cost
  (lambda (source-j)
    1))
(define substitute-cost
  (lambda (target-i source-j)
    (if (eq? target-i source-j)
        0
        2)))

(define edit-distance
  (lambda (string-a string-b)
    (let ((string-a-length (string-length string-a))
          (string-b-length (string-length string-b)))
      (cond ((and  (= string-b-length 0) (= string-a-length 0)) 0) 
            ((and (not (= string-a-length 0)) (= string-b-length 0)) string-a-length)
            ((and (not (= string-b-length 0)) (= string-a-length 0)) string-b-length)
            (else (min

                   ;; 插入
                   (+ (insert-cost (string-ref string-a (- string-a-length 1)))
                      
                      (edit-distance
                       (substring string-a 0 (- string-a-length 1))
                       string-b))

                   ;; 替换
                   (+ (substitute-cost
                       (string-ref string-a (- string-a-length 1))
                       (string-ref string-b (- string-b-length 1)))
                      
                      (edit-distance
                       (substring string-a 0 (- string-a-length 1))
                       (substring string-b 0 (- string-b-length 1))))

                   ;; 删除
                   (+ (delete-cost (string-ref string-b (- string-b-length 1)))
                      (edit-distance
                       string-a
                       (substring string-b 0 (- string-b-length 1))))))))))

(define edit-distance
  (lambda (string-a offset-a string-b offset-b)
    (cond ((and  (= offset-a 0) (= offset-b 0)) 0) 
            ((and (not (= offset-a 0)) (= offset-b 0)) offset-a)
            ((and (not (= offset-b 0)) (= offset-a 0)) offset-b)
            (else (min
                   ;; 插入
                   (+ (insert-cost (string-ref string-a (- offset-a 1)))
                      (edit-distance
                       string-a
                       (- offset-a 1)
                       string-b
                       offset-b))

                   ;; 替换
                   (+ (substitute-cost
                       (string-ref string-a (- offset-a 1))
                       (string-ref string-b (- offset-b 1)))
                      
                      (edit-distance
                       string-a
                       (- offset-a 1)
                       string-b
                       (- offset-b 1)))

                   ;; 删除
                   (+ (delete-cost (string-ref string-b (- offset-b 1)))
                      (edit-distance
                       string-a
                       offset-a
                       string-b
                       (- offset-b 1))))))))

(define uni-edit-distance
  (lambda (list-a offset-a list-b offset-b)
    (cond ((and  (= offset-a 0) (= offset-b 0)) 0) 
            ((and (not (= offset-a 0)) (= offset-b 0)) offset-a)
            ((and (not (= offset-b 0)) (= offset-a 0)) offset-b)
            (else (min
                   ;; 插入
                   (+ (insert-cost (list-ref list-a (- offset-a 1)))
                      (uni-edit-distance
                       list-a
                       (- offset-a 1)
                       list-b
                       offset-b))

                   ;; 替换
                   (+ (substitute-cost
                       (list-ref list-a (- offset-a 1))
                       (list-ref list-b (- offset-b 1)))
                      
                      (uni-edit-distance
                       list-a
                       (- offset-a 1)
                       list-b
                       (- offset-b 1)))

                   ;; 删除
                   (+ (delete-cost (list-ref list-b (- offset-b 1)))
                      (uni-edit-distance
                       list-a
                       offset-a
                       list-b
                       (- offset-b 1))))))))

(define ed (lambda (t s)
             (ed-uni
              (sort (map char->integer (string->list t))  <)
              (sort (map char->integer (string->list s))  <))))
(define ed-uni (lambda (t s)
                 (uni-edit-distance t (length t) s (length s))))
(ed "abcdaaf"
    "abcdaag")

(ed-uni
 (sort (map char->integer (string->list "asdf"))  <)
 (sort (map char->integer (string->list "afds"))  <))



(ed "hell" "hello")
(ed "helloworld" "hello world")

