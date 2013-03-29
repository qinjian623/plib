#lang racket
(require 2htdp/batch-io)
;;env should be a double hash-table list
;;first one for fields {field-name, field-ref}
;;second one for table {table-name, table-data}

(map (lambda(x) (list-ref x 3)) (filter (lambda (x) (equal? (list-ref x 13) "东北菜"))  (read-csv-file "short_test.csv")))

(define (TODO) (display "THIS FUNCTION IS ON BUILDING...HOLD ON"))

(struct select (fields from where) #:transparent)
(struct fields (lst) #:transparent)
(struct from (table) #:transparent)
(struct where (predicate) #:transparent)
(struct field (name) #:transparent)
(struct table (name)#:transparent)
(struct or (e1 e2))
(struct and (e1 e2))
(struct == (field value))
(struct <> (field value))

(define (eval-under-env e env)
  (cond [(field? e)
         (envlookup-field env (field-name e))]
        [(table? e)
         (envlookup-table env (table-name e))]
        [(from? e)
         (eval-under-env (from-table e) env)]
        [(where? e)
         (eval-under-env e env)]
        [(fields? e)
         (fields->list e env)]
        [(select? e)
         (let ([fields (eval-under-env (select-fields e) env)]
               [where (eval-under-env (select-where e) env)]
               [table (eval-under-env (select-from e) env)])
           (map (filter-fields-func fields) (filter (where-func where) table)))]
        [(or? e)
         (let ([e1 (eval-under-env (or-e1 e) env)]
               [e2 (eval-under-env (or-e2 e) env)])
           (TODO))]
        [(and? e) (TODO)]
        [(== e) (TODO)]
        [(<> e) (TODO)]
        [#t (error "bad expression or any syntax that my interpreter can't handle yet")]))


;;TODO test
(define (filter-fields-func fields)
  (lambda (x)
    (map (lambda (field) (list-ref x field)) fields)))
;;TODO test
(define (envlookup-field env name) (hash-ref (first env) name))
;;TODO test
(define (envlookup-table env name) (hash-ref (second env) name))
;;TODO test
(define (fields->list e env)
  (map (lambda (field) (envlookup-field env (field-name field)))))




