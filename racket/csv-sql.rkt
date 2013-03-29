#lang racket
(require 2htdp/batch-io)
;;env should be a double hash-table list
;;first one for fields {field-name, field-ref}
;;second one for table {table-name, table-data}

(define (TODO) (display "THIS FUNCTION IS ON BUILDING...HOLD ON"))

(struct select (fields from where) #:transparent)
(struct fields (lst) #:transparent)
(struct from (table) #:transparent)
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
         (envlookup-field env (field-name e))]
        [(table? e)
         (envlookup-table env (table-name e))]
        [(from? e)
         (eval-under-env (from-table e) env)]
        [(where? e)
         (begin (display "interpeter in: where\n")
                (display e)
                (display "\n")
                (eval-under-env (where-predicate e) env))]
        [(fields? e)
         (fields->list e env)]
        [(value? e)
         (value-v e)]
        [(select? e)
         (let ([fields (eval-under-env (select-fields e) env)]
               [where (eval-under-env (select-where e) env)]
               [table (eval-under-env (select-from e) env)])
           (map (filter-fields-func fields) (filter (where-predicate where) table)))]
        [(qor? e)
         (let ([e1 (eval-under-env (qor-e1 e) env)]
               [e2 (eval-under-env (qor-e2 e) env)])
           (lambda(data)(or (e1 data) (e2 data))))]
        [(qand? e) 
         (let ([e1 (eval-under-env (qand-e1 e) env)]
               [e2 (eval-under-env (qand-e2 e) env)])
           (lambda(data)(and (e1 data) (e2 data))))]
        [(q==? e) (let([f (eval-under-env (q==-field e) env)]
                      [v (eval-under-env (q==-value e) env)])
                   (lambda (data)(equal? (list-ref data f) v)))]
        [(q<>? e) (let([f (eval-under-env (q==-field e) env)]
                      [v (eval-under-env (q==-value e) env)])
                   (lambda (data)(not (equal? (list-ref data f) v))))]
        [#t (error "bad expression or any syntax that my interpreter can't handle yet")]))

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

(define (envlookup-table env name) (hash-ref (second env) name))

(define (fields->list e env)
  (map (lambda (field) (envlookup-field env (field-name field))) (fields-lst e)))

(eval (select
       (fields (list (field "NID")
                     (field "STRNAME")))
       (from (table "t"))
       (where (q== (field "NID")
                   (value "910002097"))))
      "c:\\short_test.csv" "t")

(list-ref (first (hash-ref (second (make-env "c:\\short_test.csv" "t")) "t"))
          0)
(take (hash-ref (second (make-env "c:\\short_test.csv" "t")) "t") 5)
(map (lambda(x) (list-ref x 3)) (filter (lambda (x) (equal? (list-ref x 13) "东北菜"))  (read-csv-file "c:\\short_test.csv")))
