import { useEffect, useState } from 'react';
import { database, auth } from '../firebase';
import { ref, get } from 'firebase/database';

const useAdmin = () => {
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const checkAdmin = async () => {
      try {
        if (!auth.currentUser) {
          setIsAdmin(false);
          return;
        }

        const adminRef = ref(database, `admins/${auth.currentUser.uid}`);
        const snapshot = await get(adminRef);
        setIsAdmin(snapshot.exists());
      } catch (error) {
        console.error('Error checking admin status:', error);
        setIsAdmin(false);
      }
    };

    checkAdmin();
  }, []);

  return isAdmin;
};

export default useAdmin;
