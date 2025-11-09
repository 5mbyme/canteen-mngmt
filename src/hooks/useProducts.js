import { useEffect, useState } from 'react';
import { database } from '../firebase';
import { ref, onValue } from 'firebase/database';

const useProducts = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const productsRef = ref(database, 'products');
    
    const unsubscribe = onValue(productsRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        const productsList = Object.entries(data).map(([key, value]) => ({
          ...value,
          id: value.id || key,
        }));
        setProducts(productsList);
      } else {
        setProducts([]);
      }
    });

    return () => unsubscribe();
  }, []);

  const updateProductQuantity = (productId, newQuantity) => {
    setProducts(prevProducts =>
      prevProducts.map(p =>
        p.id === productId ? { ...p, quantity: newQuantity } : p
      )
    );
  };

  return { products, updateProductQuantity };
};

export default useProducts;
