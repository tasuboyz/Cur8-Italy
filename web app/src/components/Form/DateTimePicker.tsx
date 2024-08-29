import React from 'react';
import '../../App.css'

interface DateTimePickerProps {
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const DateTimePicker: React.FC<DateTimePickerProps> = ({ value, onChange }) => {
  return (
    <div>
      <input
        type="datetime-local"
        id="dateTime"
        value={value}
        onChange={onChange}
        className="form-control"
      />
    </div>
  );
};

export default DateTimePicker;
