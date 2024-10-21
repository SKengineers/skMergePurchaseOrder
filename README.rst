Merge Purchase Order
=========
When we install this module, these feature will appear

* In list view of Purchase Order, we can select multiple Purchase Order for merging
We have 4 types of merge purchase order


* Create new Order and Cancel all selected Order: Cancel all of selected purchase order and create new purchase order for all of product
* Create new Order and Delete all selected Order: Delete all of selected purchase order and create new purchase order for all of product
* Merge order into selected Order and cancel: We can select purchase order that will combine all of data of the others purchase, and then cancel the others
* Merge order into selected Order and delete: We can select purchase order that will combine all of data of the others purchase, and then delete the others

Notes: All of purchase order need in state != 'cancel' and 'order' and it need in the same VENDOR. Otherwise, it will raise Error