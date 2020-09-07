CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`%` 
    SQL SECURITY DEFINER
VIEW `post_library`.`v_post_lite` AS
    SELECT 
        `post_library`.`post`.`description` AS `description`,
        `post_library`.`post`.`price` AS `price`,
        (SELECT 
                `post_library`.`telephone`.`number`
            FROM
                `post_library`.`telephone`
            WHERE
                (`post_library`.`telephone`.`uuid` = (SELECT 
                        `post_library`.`telephone__post`.`uuid_telephone`
                    FROM
                        `post_library`.`telephone__post`
                    WHERE
                        (`post_library`.`telephone__post`.`uuid_post` = `post_library`.`post`.`uuid`)
                    LIMIT 1))) AS `num_telephone`,
        `post_library`.`country`.`title` AS `title_country`,
        `post_library`.`city`.`title` AS `title_city`,
        `post_library`.`address`.`title` AS `title_address`,
        `post_library`.`address`.`latitude` AS `latitude`,
        `post_library`.`address`.`longitude` AS `longitude`,
        (SELECT 
                `post_library`.`img`.`url`
            FROM
                `post_library`.`img`
            WHERE
                (`post_library`.`img`.`uuid` = (SELECT 
                        `post_library`.`img__post`.`uuid_img`
                    FROM
                        `post_library`.`img__post`
                    WHERE
                        (`post_library`.`img__post`.`uuid_post` = `post_library`.`post`.`uuid`)
                    LIMIT 1))) AS `url_img`,
        (SELECT 
                `post_library`.`link`.`datetime`
            FROM
                `post_library`.`link`
            WHERE
                (`post_library`.`link`.`uuid_post` = `post_library`.`post`.`uuid`)
            ORDER BY `post_library`.`link`.`datetime` DESC
            LIMIT 1) AS `datecreate`
    FROM
        (((`post_library`.`post`
        JOIN `post_library`.`address` ON ((`post_library`.`post`.`uuid_address` = `post_library`.`address`.`uuid`)))
        JOIN `post_library`.`city` ON ((`post_library`.`address`.`uuid_city` = `post_library`.`city`.`uuid`)))
        JOIN `post_library`.`country` ON ((`post_library`.`city`.`uuid_country` = `post_library`.`country`.`uuid`)))
    HAVING ((`datecreate` IS NOT NULL)
        AND (`url_img` IS NOT NULL)
        AND (`num_telephone` IS NOT NULL))
    ORDER BY `datecreate` DESC