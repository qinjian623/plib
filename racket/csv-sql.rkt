#lang racket
(require 2htdp/batch-io)
;;env should be a double hash-table list
;;first one for fields {field-name, field-ref}
;;second one for table {table-name, table-data}

(define (TODO) (display "THIS FUNCTION IS ON BUILDING...HOLD ON"))
(define (log msg) (begin
                    (display msg)
                    (display "\n")))
;;(define (log msg) '())

(struct select (fields from where) #:transparent)
(struct delete (from where) #:transparent)
(struct insert (into fields values) #:transparent)
(struct fields (lst) #:transparent)
(struct values (lst) #:transparent)
(struct from (table) #:transparent)
(struct into (table) #:transparent)
(struct where (predicate) #:transparent)
(struct field (name) #:transparent)
(struct table (name) #:transparent)
(struct qor (e1 e2) #:transparent)
(struct qand (e1 e2) #:transparent)
(struct q== (field value) #:transparent)
(struct q<> (field value) #:transparent)
(struct value (v) #:transparent)

(define (eval-under-env e env)
  (cond [(field? e)
         (begin (log "field")
                (log e)
                (envlookup-field env (field-name e)))]
        [(table? e)
         (begin (log "table")
                (log e)
                (envlookup-table env (table-name e)))]
        [(from? e)
         (begin (log "from")
                (log e)
                (eval-under-env (from-table e) env))]
        [(into? e)
         (begin (log "into")
                (log e)
                (eval-under-env (into-table e) env))]
        [(where? e)
         (begin (log "where")
                (log e)
                (eval-under-env (where-predicate e) env))]
        [(fields? e)
         (begin (log "fields")
                (log e)
                (fields->list e env))]
        [(values? e)
         (begin (log "values")
                (log e)
                (map value-v (values-lst e)))]
        [(value? e)
         (begin (log "value")
                (log e)
                (value-v e))]
        [(select? e)
         (begin (log "select")
                (log e)
                (let ([fields (eval-under-env (select-fields e) env)]
                      [where (eval-under-env (select-where e) env)]
                      [table (eval-under-env (select-from e) env)])
                  (map (filter-fields-func fields)
                       (filter where table))))]
        ;; TODO how to store the new table into the env??
        [(delete? e)
         (begin (log "delete")
                (log e)
                (let* ([table (eval-under-env (delete-from e) env)]
                      [where (eval-under-env (delete-where e) env)]
                      [new-table (filter (lambda (data) (not (where data))) table)])
                  new-table))]
        [(insert? e)
         (begin (log "insert")
                (log e)
                (let* ([table (eval-under-env (insert-into e) env)]
                       [fields (eval-under-env (insert-fields e) env)]
                       [values (eval-under-env (insert-values e) env)]
                       [new-row (fields*values->row fields values (first table))])
                  (cons new-row table)))]
        ;; TODO ...
        [(update? e)
         ]
        [(qor? e)
         (begin (log "qor")
                (log e)
                (let ([e1 (eval-under-env (qor-e1 e) env)]
                      [e2 (eval-under-env (qor-e2 e) env)])
                  (lambda(data)(or (e1 data) (e2 data)))))]
        [(qand? e)
         (begin (log "qand")
                (log e)
                (let ([e1 (eval-under-env (qand-e1 e) env)]
                      [e2 (eval-under-env (qand-e2 e) env)])
                  (lambda(data)(and (e1 data) (e2 data)))))]
        [(q==? e)
         (begin (log "q==")
                (log e)
                (let([f (eval-under-env (q==-field e) env)]
                     [v (eval-under-env (q==-value e) env)])
                  (lambda (data)(equal? (list-ref data f) v))))]
        [(q<>? e)
         (begin (log "q<>")
                (log e)
                (let([f (eval-under-env (q<>-field e) env)]
                     [v (eval-under-env (q<>-value e) env)])
                  (lambda (data)(not (equal? (list-ref data f) v)))))]
        [#t (error "bad expression or any syntax that my interpreter can't handle yet")]))


(define (fields*values->row f v example)
  (let* ([len (length example)]
         [new-row (make-vector len "")])
    (begin
      (map (lambda (f v) (vector-set! new-row f v)) f v)
      (vector->list new-row))))

(define (eval e csv-name table-name)
  (eval-under-env e (make-env csv-name table-name)))

(define (load-csv name)
  (read-csv-file name))

(define (make-env csv-name table-name)
  (let* ([t (make-hash)]
        [all (load-csv csv-name)]
        [head (first all)]
        [body (drop all 1)])
    (begin
      (hash-set! t table-name body)
      (list (head->fields head) t))))

(define (head->fields head)
  (let ([v (range (count (lambda (x) true) head))])
    (make-hash(map (lambda (x y) (cons x y)) head v))))


(define (filter-fields-func fields)
  (lambda (x)
    (map (lambda (field) (list-ref x field)) fields)))

(define (envlookup-field env name) (hash-ref (first env) name))
;;TODO for setting the table
(define (envsetup-field env name value)
  ())
(define (envlookup-table env name) (hash-ref (second env) name))

(define (fields->list e env)
  (map (lambda (field) (envlookup-field env (field-name field))) (fields-lst e)))



;;; Test cases below:
(eval (select
       (fields (list (field "NID")
                     (field "STRNAME")
                     (field "GBCITYCODE")))
       (from (table "t"))
       (where (q== (field "NID")
                   (value "910002097"))))
      "c:\\short_test.csv" "t")
(eval (delete
       (from (table "t"))
       (where (q<> (field "NID")
                   (value "910002097"))))
      "c:\\short_test.csv" "t")
(eval (insert
       (into (table "t"))
       (fields (list (field "NID") (field "STRNAME")))
       (values (list (value "1010") (value "haha"))))
      "c:\\short_test.csv" "t")

(list-ref (first (hash-ref (second (make-env "c:\\short_test.csv" "t")) "t")) 0)
(take (hash-ref (second (make-env "c:\\short_test.csv" "t")) "t") 1)
(map (lambda(x) (list-ref x 3)) (filter (lambda (x) (equal? (list-ref x 13) "东北菜"))  (read-csv-file "c:\\short_test.csv")))

(define (cached-assoc xs n)
  (letrec ([memo (make-vector n #f)]
           [pos 0]
           [f (lambda (v) (let ([r (vector-assoc v memo)])
                           (if r
                               r
                               (let ([list-p (assoc v xs)])
                                 (if list-p
                                     (begin
                                       (vector-set! memo pos list-p)
                                       (if (= (+ pos 1) n)
                                           (set! pos 0)
                                           (set! pos (+ pos 1)))
                                       list-p)
                                     #f
                                 )))))]) f))
