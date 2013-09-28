;;1.2.1 list-length
(define list-length
  (lambda (lst)
    (if (null? lst)
        0
        (+ 1 (list-length (cdr lst))))))

;;1.2.2 nth-element
(define nth-element
  (lambda (lst n)
    (if (null? lst)
        (report-list-too-short n)
        (if (zero? n)
            (car lst)
            (nth-element (cdr lst) (- n 1))))))

;;1.2.3 remove-first
(define remove-first
  (lambda (sym lst)
    (if (null? lst)
        '()
        (if (equal? (car lst) sym)
            (cdr lst)
            (cons (car lst) (remove-first sym (cdr lst)))))))
;;1.2.4 occurs-free?
(define occurs-free?
  (lambda (var exp)
    (cond
     ((symbol? exp) (eqv? var exp))
     ((eqv? (car exp) ’lambda)
      (and
       (not (eqv? var (car (cadr exp))))
       (occurs-free? var (caddr exp))))
     (else
      (or
       (occurs-free? var (car exp))
       (occurs-free? var (cadr exp)))))))
;;1.2.5 subst
(define subst
  (lambda (new old slist)
    (if (null? slist)
        '()
        (cons
         (subst-in-s-exp new old (car slist))
         (subst new old (cdr slist))))))
(define subst-in-s-exp
  (lambda (new old sexp)
    (if (symbol? sexp)
        (if (eqv? sexp old) new sexp)
        (subst new old sexp))))

;;1.3
(define number-elements
  (lambda (lst)
    (number-elements-from lst 0)))
(define number-elements-from
  (lambda (lst n)
    (if (null? lst)
        '()
        (cons (list n (car lst)) (number-elements-from (cdr lst) (+ 1 n))))))
(define list-sum
  (lambda (slist)
    ))




(define report-list-too-short
  (lambda (n)
    (eopl:error ’nth-element
                  "List too short by ~s elements.~%" (+ n 1))))

