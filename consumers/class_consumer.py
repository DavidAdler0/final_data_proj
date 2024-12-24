from sqlalchemy.exc import SQLAlchemyError

from consumers.consumer_service import decode_kafka_message, create_consumer
from database import db_session
from models.classes import Class




def process_class_messages(sql_consumer):
    try:
        for message in sql_consumer:
            row = decode_kafka_message(message)
            if not row.get('course_name'):
                print(f"the following line is not a class {row}")
                continue
            new_class = Class(**row)
            class_exists = db_session.query(Class).filter(Class.id == new_class.id).first()
            if class_exists:
                print(f"teacher {new_class.id} already exists")
                continue
            db_session.add(new_class)
            db_session.commit()
        sql_consumer.commit()
        return None
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error processing message: {e}")

def main():
    class_consumer = create_consumer('classes')
    process_class_messages(class_consumer)

if __name__ == '__main__':
    main()