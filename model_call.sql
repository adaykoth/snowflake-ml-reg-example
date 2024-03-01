CREATE OR REPLACE TEMP TABLE t1 AS
SELECT core.test.model1!predict(0.1,0.1,0.1):pred_d AS model1,
        core.test.model2!predict(0.1,0.1,0.1):pred_d AS model2,
        1 as id;

CREATE OR REPLACE TEMP TABLE t2 AS
SELECT core.test.model2!predict(0.1,0.1,0.1):pred_d as model2,
        core.test.model1!predict(0.1,0.1,0.1):pred_d AS model1,
        1 as id;

SELECT
    (t1.model1 - t2.model1) AS diff_model1,
    (t1.model2 - t2.model2) AS diff_model2
FROM
    t1
JOIN
    t2 USING (id);
