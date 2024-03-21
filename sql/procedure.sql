-- Show product and order by name
DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS DisplayProductsOrderbyName()
BEGIN
    SELECT * FROM Products ORDER BY Name;
END$$

DELIMITER ;

-- Search product order
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS SearchbyProductandOrder(
	IN pName varchar(100),
    IN pPrice varchar (100)
)
BEGIN 
IF pPrice = "DESC" THEN
	select * from products
    where name LIKE CONCAT("%", pName, "%")
    order by price desc;
ELSEIF  pPrice = "ASC" THEN
	select * from products
    where name LIKE CONCAT("%", pName, "%")
    order by price asc;
ELSE
	select * from products
    where name LIKE CONCAT("%", pName, "%");
END IF;
END //
DELIMITER ;

-- Make procedure to insert Customer
DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS InsertCustomer(
    IN p_Username VARCHAR(50),
    IN p_Email VARCHAR(100),
    IN p_Password VARCHAR(100),
    IN p_FullName VARCHAR(100),
    IN p_Address TEXT,
    IN p_PhoneNumber VARCHAR(20),
    IN p_IsSeller BOOLEAN
)
BEGIN
    INSERT INTO Users (Username, Email, Password, FullName, Address, PhoneNumber, IsSeller) VALUES
    (p_Username, p_Email, p_Password, p_FullName, p_Address, p_PhoneNumber, p_IsSeller);
END$$
DELIMITER ;

-- Make procedure to insert Transaction
DELIMITER $$
CREATE PROCEDURE IF NOT EXISTS InsertTransaction(
    IN p_UserID INT,
    IN p_ShippingAddress TEXT,
    IN p_TotalPrice DECIMAL(10, 2),
    IN p_Status VARCHAR(50)
)
BEGIN
    INSERT INTO Orders (UserID, ShippingAddress, TotalPrice, Status) VALUES 
    (p_UserID, p_ShippingAddress, p_TotalPrice, p_Status);
END$$
DELIMITER ;

-- Apply discount to Product
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS ApplyDiscountToProduct(
    IN pProductID INT,
    IN pDiscountPercentage DECIMAL(5, 2)
)
BEGIN
    DECLARE originalPrice DECIMAL(10, 2);
	DECLARE discountedPrice DECIMAL(10, 2);    
    -- Mengambil harga asli produk
    SELECT Price INTO originalPrice
    FROM Products
    WHERE ProductID = pProductID;

    -- Menghitung harga baru setelah diberikan diskon

    SET discountedPrice = originalPrice - (originalPrice * (pDiscountPercentage / 100));

    -- Update harga produk dengan diskon
    UPDATE Products
    SET Price = discountedPrice
    WHERE ProductID = pProductID;
END //

DELIMITER ;

-- Add to Cart
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS AddToCart(
    IN pUserID INT,
    IN pProductID INT,
    IN pQuantity INT
)
BEGIN
    DECLARE totalPrice DECIMAL(10, 2);

    -- Menghitung total harga berdasarkan harga produk dan jumlah pesanan
    SELECT Price * pQuantity INTO totalPrice
    FROM Products
    WHERE ProductID = pProductID;

    -- Menambahkan produk ke dalam keranjang belanja pengguna
    INSERT INTO CartDetails (CartID, ProductID, Quantity, Price)
    VALUES ((SELECT CartID FROM Cart WHERE UserID = pUserID), pProductID, pQuantity, totalPrice);
END //

DELIMITER ;

-- Add new Product
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS AddProduct(
    IN seller_id INT,
    IN name VARCHAR(100),
    IN description TEXT,
    IN price DECIMAL(10, 2),
    IN stock INT,
    IN category_id INT
)
BEGIN
    INSERT INTO Products (SellerID, Name, Description, Price, Stock, CategoryID)
    VALUES (seller_id, name, description, price, stock, category_id);
END //

DELIMITER ;